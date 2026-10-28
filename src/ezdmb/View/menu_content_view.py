# pylint: disable=no-name-in-module
import logging
from datetime import UTC, datetime
from threading import Event
from time import monotonic

from PySide6.QtCore import QPoint, QThread, Signal, Slot
from PySide6.QtGui import QFont, QPainter, QPixmap, Qt

from ezdmb.Controller.configuration import (
    configuration,
    default_content_groups,
    default_time_blocks,
)
from ezdmb.Utility.media_utility import convert_presentation_to_pdf, get_content_type


class menu_content_view(QThread):
    contentUpdated = Signal(QPixmap)
    videoUpdated = Signal(str)
    pdfUpdated = Signal(str)
    webUpdated = Signal(str)

    def __init__(
        self,
        config: configuration,
        pixmap,
        windowName,
        onRefresh,
        onVideoRefresh=None,
        onPdfRefresh=None,
        onWebRefresh=None,
    ):
        QThread.__init__(self)
        self._config = config
        self._stop_event = Event()
        self._wake_event = Event()
        self._active_video_path = None

        self.debug = True
        self.contentArray = self._config.ContentArray
        self.contentGroups = getattr(
            self._config,
            "ContentGroups",
            default_content_groups(self.contentArray),
        )
        self.timeBlocks = getattr(
            self._config,
            "TimeBlocks",
            default_time_blocks(),
        )
        self.rotationMode = getattr(
            self._config,
            "RotationMode",
            "interval" if self._config.RotateContent else "none",
        )
        self.rotateContent = self.rotationMode == "interval"
        self.rotateTimeout = self._config.RotateContentTime
        self.count = 0
        self.pixmap = pixmap
        self.windowName = windowName
        self.contentUpdated.connect(onRefresh)
        if onVideoRefresh is not None:
            self.videoUpdated.connect(onVideoRefresh)
        if onPdfRefresh is not None:
            self.pdfUpdated.connect(onPdfRefresh)
        if onWebRefresh is not None:
            self.webUpdated.connect(onWebRefresh)
        self._config.configUpdated.connect(self.onConfigUpdated)
        self.start()

    def stop(self):
        self._stop_event.set()
        self._wake_event.set()
        self.wait()

    @Slot(dict)
    def onConfigUpdated(self, data):
        self.contentGroups = data.get(
            "content_groups",
            default_content_groups(data.get("imported_content", [])),
        )
        self.contentArray = [
            content
            for group in self.contentGroups
            for content in group["content"]
        ]
        self.timeBlocks = data.get("time_blocks", default_time_blocks())
        self.rotationMode = data.get(
            "rotation_mode",
            "interval" if data.get("rotate_content", True) else "none",
        )
        if self.rotationMode not in ("interval", "schedule", "none"):
            raise ValueError(f"Unsupported rotation mode: {self.rotationMode}")
        self.rotateContent = self.rotationMode == "interval"
        self.rotateTimeout = data["rotate_content_time"]
        self._wake_event.set()

    def getViewableFilecontent(self, fileName):
        content_type = get_content_type(fileName)
        if content_type == "image":
            return QPixmap(fileName)
        elif content_type == "text":
            with open(fileName, "r") as f:
                txt_content = f.read()
                pix = QPixmap(400, 300)
                pix.fill(Qt.GlobalColor.white)
                painter = QPainter(pix)
                painter.setFont(QFont("Arial"))

                row_spacing = 20
                i = 1
                for line in txt_content.splitlines():
                    painter.drawText(QPoint(12, i * row_spacing), line)
                    i += 1

                return pix
        else:
            return None

    def run(self):
        current_mode = None
        current_group_id = None
        current_items = []
        current_index = 0
        next_rotation_at = 0.0

        while not self._stop_event.is_set():
            self._wake_event.clear()
            mode = self.rotationMode
            now = datetime.now(tz=UTC).astimezone()
            now_monotonic = monotonic()
            rotate_timeout = max(float(self.rotateTimeout), 1)

            if mode == "interval":
                items = self.contentArray
                if mode != current_mode or items != current_items:
                    current_mode = mode
                    current_group_id = None
                    current_items = list(items)
                    current_index = 0
                    next_rotation_at = 0.0

                if items and now_monotonic >= next_rotation_at:
                    index = self.display_index(current_index, items)
                    current_index = (current_index + 1) % len(items)
                    next_rotation_at = now_monotonic + rotate_timeout
                    if self.debug:
                        print(
                            self.windowName
                            + ": Displaying content "
                            + str(index + 1)
                            + " of "
                            + str(len(items))
                        )
                    wait_time = rotate_timeout
                else:
                    wait_time = (
                        min(1.0, rotate_timeout)
                        if not items
                        else max(0.1, next_rotation_at - now_monotonic)
                    )
            elif mode == "none":
                items = self.contentArray
                if mode != current_mode or items != current_items:
                    current_mode = mode
                    current_group_id = None
                    current_items = list(items)
                    current_index = 0
                    if items:
                        self.display_index(0, items)
                    print("Rotation is disabled; Showing first content in the list.")
                wait_time = 1.0
            elif mode == "schedule":
                if mode != current_mode:
                    current_mode = mode
                    current_group_id = None
                    current_items = []
                    current_index = 0
                    next_rotation_at = 0.0

                group = self.getScheduledGroup(now)
                if group is None:
                    current_group_id = None
                    current_items = []
                    wait_time = self._secondsUntilNextScheduleBlock(now)
                else:
                    items = group["content"]
                    if group["id"] != current_group_id or items != current_items:
                        current_group_id = group["id"]
                        current_items = list(items)
                        current_index = 0
                        next_rotation_at = 0.0

                    if items and now_monotonic >= next_rotation_at:
                        self.display_index(current_index, items)
                        current_index = (current_index + 1) % len(items)
                        next_rotation_at = now_monotonic + rotate_timeout
                    wait_time = min(
                        self._secondsUntilNextScheduleBlock(now),
                        max(0.1, next_rotation_at - now_monotonic)
                        if items
                        else self._secondsUntilNextScheduleBlock(now),
                    )
            else:
                raise ValueError(f"Unsupported rotation mode: {mode}")

            self._wake_event.wait(wait_time)

    def getScheduledGroup(self, current_time=None):
        if current_time is None:
            current_time = datetime.now(tz=UTC).astimezone()

        repeat_mode = self.timeBlocks["repeat"]
        if repeat_mode == "Daily":
            blocks = self.timeBlocks["daily"]
        elif repeat_mode == "Weekly":
            blocks = self.timeBlocks["weekly"].get(
                current_time.strftime("%A"),
                [],
            )
        elif repeat_mode == "None":
            blocks = self.timeBlocks["dated"].get(
                current_time.date().isoformat(),
                [],
            )
        else:
            raise ValueError(f"Unsupported schedule repeat mode: {repeat_mode}")

        active_group_ids = {
            block["group_id"]
            for block in blocks
            if self._isTimeBlockActive(block, current_time)
        }
        return next(
            (
                group
                for group in self.contentGroups
                if group["id"] in active_group_ids
            ),
            None,
        )

    @staticmethod
    def _isTimeBlockActive(block, current_time):
        start = menu_content_view._timeStringToMinutes(block["start"])
        end = menu_content_view._timeStringToMinutes(block["end"])
        current_minutes = current_time.hour * 60 + current_time.minute
        return start <= current_minutes < end

    @staticmethod
    def _timeStringToMinutes(value):
        hours, minutes = (int(part) for part in value.split(":"))
        total_minutes = hours * 60 + minutes
        if not 0 <= total_minutes <= 24 * 60:
            raise ValueError(f"Invalid time block boundary: {value}")
        return total_minutes

    @staticmethod
    def _secondsUntilNextScheduleBlock(current_time):
        seconds_into_slot = (
            current_time.minute % 30
        ) * 60 + current_time.second + current_time.microsecond / 1_000_000
        return max(0.1, 30 * 60 - seconds_into_slot)

    def display_index(self, i, content_array=None):
        content_array = self.contentArray if content_array is None else content_array
        index = i % len(content_array)
        content_path = content_array[index]
        content_type = get_content_type(content_path)
        if content_type in ("video", "pdf", "web", "presentation"):
            if content_path != self._active_video_path:
                self._active_video_path = content_path
                if content_type == "video":
                    self.videoUpdated.emit(content_path)
                elif content_type == "web":
                    self.webUpdated.emit(content_path.strip())
                else:
                    pdf_path = content_path
                    if content_type == "presentation":
                        try:
                            pdf_path = convert_presentation_to_pdf(content_path)
                        except Exception:  # pylint: disable=broad-except
                            logging.getLogger(__name__).exception(
                                "Unable to convert presentation: %s", content_path
                            )
                            self._active_video_path = None
                            return index
                    self.pdfUpdated.emit(pdf_path)
            return index

        self._active_video_path = None
        img = self.getViewableFilecontent(content_path)
        if img is not None:
            self.contentUpdated.emit(img)
        return index
