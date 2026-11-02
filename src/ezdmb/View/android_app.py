"""Single-window, touch-first Android application views."""

import logging
import os
from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Qt, QUrl
from PySide6.QtGui import QGuiApplication, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QScroller,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ezdmb.Controller.configuration import configuration
from ezdmb.Utility.android_storage_utility import android_storage_utility
from ezdmb.Utility.bundle_utility import (
    export_bundle,
    import_bundle,
    import_bundle_from_url,
)
from ezdmb.Utility.path_utility import is_android
from ezdmb.View.config_widget import config_widget
from ezdmb.View.menu_content_view import menu_content_view

if TYPE_CHECKING:
    from PySide6 import QtPdf as _QtPdf  # noqa: F401
    from PySide6 import QtPdfWidgets as _QtPdfWidgets  # noqa: F401
    from PySide6 import QtSvg as _QtSvg  # noqa: F401


_logger = logging.getLogger(__name__)


def _qt_type(module_name: str, type_name: str):
    try:
        return getattr(import_module(module_name), type_name)
    except (ImportError, AttributeError, OSError) as error:
        _logger.info(
            "Qt type %s.%s is unavailable: %s",
            module_name,
            type_name,
            error,
        )
        return None


class android_display_widget(QWidget):
    def __init__(self, config: configuration, parent=None):
        super().__init__(parent)
        self._shutdown = False
        self._video_player_class = None
        audio_output_class = None
        video_widget_class = None
        if not is_android():
            self._video_player_class = _qt_type(
                "PySide6.QtMultimedia",
                "QMediaPlayer",
            )
            audio_output_class = _qt_type(
                "PySide6.QtMultimedia",
                "QAudioOutput",
            )
            video_widget_class = _qt_type(
                "PySide6.QtMultimediaWidgets",
                "QVideoWidget",
            )
        self._pdf_document_class = _qt_type(
            "PySide6.QtPdf",
            "QPdfDocument",
        )
        pdf_view_class = _qt_type(
            "PySide6.QtPdfWidgets",
            "QPdfView",
        )

        self.contentStack = QStackedWidget(self)
        self.contentStack.setObjectName("androidContentStack")
        self.contentLbl = QLabel(self.contentStack)
        self.contentLbl.setObjectName("androidContentLabel")
        self.contentLbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contentLbl.setWordWrap(True)
        self.contentLbl.setScaledContents(True)
        self.contentLbl.setStyleSheet(
            "background-color: black; color: white; padding: 24px;"
        )
        self.contentStack.addWidget(self.contentLbl)

        self.videoWidget = None
        self.videoPlayer = None
        self.audioOutput = None
        if (
            self._video_player_class is not None
            and audio_output_class is not None
            and video_widget_class is not None
        ):
            self.videoWidget = video_widget_class(self.contentStack)
            self.videoWidget.setAspectRatioMode(
                Qt.AspectRatioMode.KeepAspectRatio
            )
            self.contentStack.addWidget(self.videoWidget)
            self.audioOutput = audio_output_class(self)
            self.videoPlayer = self._video_player_class(self)
            self.videoPlayer.setAudioOutput(self.audioOutput)
            self.videoPlayer.setVideoOutput(self.videoWidget)
            self.videoPlayer.setLoops(
                self._video_player_class.Loops.Infinite
            )
            self.videoPlayer.errorOccurred.connect(self.onVideoError)

        self.pdfDocument = None
        self.pdfView = None
        if self._pdf_document_class is not None and pdf_view_class is not None:
            self.pdfDocument = self._pdf_document_class(self)
            self.pdfView = pdf_view_class(self.contentStack)
            self.pdfView.setDocument(self.pdfDocument)
            self.pdfView.setPageMode(pdf_view_class.PageMode.MultiPage)
            self.pdfView.setZoomMode(pdf_view_class.ZoomMode.FitToWidth)
            self.pdfDocument.statusChanged.connect(self.onPdfStatusChanged)
            self.contentStack.addWidget(self.pdfView)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.contentStack)

        self.contentViewUtil = menu_content_view(
            config,
            self.contentLbl,
            "android_display",
            self.onRefresh,
            self.onVideoRefresh,
            self.onPdfRefresh,
            self.onWebRefresh,
        )
        if isinstance(self.contentViewUtil, QObject):
            self.contentViewUtil.setParent(self)
        self.contentViewUtil.errorUpdated.connect(self.onContentError)

        app = QApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(self.shutdown)

    def onRefresh(self, pixmap: QPixmap):
        self._stop_video()
        self.contentLbl.clear()
        self.contentLbl.setPixmap(pixmap)
        self.contentStack.setCurrentWidget(self.contentLbl)

    def onVideoRefresh(self, value: str):
        self._stop_video()
        if self.videoPlayer is None or self.videoWidget is None:
            self.onContentError(
                "Video playback is not available in this Android build."
            )
            return
        if not Path(value).is_file():
            self.onContentError(f"Video file is unavailable: {Path(value).name}")
            return

        self.contentLbl.clear()
        self.videoPlayer.setSource(
            QUrl.fromLocalFile(os.path.abspath(value))
        )
        self.contentStack.setCurrentWidget(self.videoWidget)
        self.videoPlayer.play()

    def onPdfRefresh(self, value: str):
        self._stop_video()
        if self.pdfDocument is None or self.pdfView is None:
            self.onContentError(
                "PDF viewing is not available in this Android build."
            )
            return
        if not Path(value).is_file():
            self.onContentError(f"PDF file is unavailable: {Path(value).name}")
            return

        self.contentLbl.clear()
        status = self.pdfDocument.load(os.path.abspath(value))
        if status == self._pdf_document_class.Status.Error:
            self.onContentError(f"Unable to load PDF: {Path(value).name}")
            return
        self.contentStack.setCurrentWidget(self.pdfView)

    def onWebRefresh(self, _value: str):
        self._stop_video()
        self.onContentError(
            "Web pages cannot be rendered on Android because Qt WebEngine "
            "Widgets is not available for this platform."
        )

    def onPdfStatusChanged(self, status):
        if (
            self._pdf_document_class is not None
            and status == self._pdf_document_class.Status.Error
        ):
            self.onContentError("Unable to load the selected PDF.")

    def onVideoError(self, _error, error_message: str):
        _logger.error("Android video playback failed: %s", error_message)
        self.onContentError(
            "Unable to play this video on this device. "
            "The supported codecs depend on Android."
        )

    def onContentError(self, message: str):
        self._stop_video()
        self.contentLbl.setTextFormat(Qt.TextFormat.PlainText)
        self.contentLbl.setPixmap(QPixmap())
        self.contentLbl.setText(message)
        self.contentStack.setCurrentWidget(self.contentLbl)

    def pause(self):
        self.contentViewUtil.pause()
        if self.videoPlayer is not None:
            self.videoPlayer.pause()

    def resume(self):
        self.contentViewUtil.resume()
        if (
            self.videoPlayer is not None
            and self.videoWidget is not None
            and self.contentStack.currentWidget() is self.videoWidget
        ):
            self.videoPlayer.play()

    def shutdown(self):
        if self._shutdown:
            return
        self._shutdown = True
        self.contentViewUtil.stop()
        if self.videoPlayer is not None:
            self.videoPlayer.stop()

    def _stop_video(self):
        if self.videoPlayer is not None:
            self.videoPlayer.stop()


class android_display_page(QWidget):
    def __init__(self, config: configuration, show_settings, parent=None):
        super().__init__(parent)
        self.display = android_display_widget(config, self)
        self.settingsButton = QPushButton("Settings", self)
        self.settingsButton.setObjectName("androidSettingsButton")
        self.settingsButton.setAccessibleName("Open Settings")
        self.settingsButton.setMinimumSize(132, 56)
        self.settingsButton.clicked.connect(show_settings)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.display, 0, 0)
        layout.addWidget(
            self.settingsButton,
            0,
            0,
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom,
        )


class android_app_window(QMainWindow):
    def __init__(
        self,
        config: configuration,
        storage_adapter: android_storage_utility,
        parent=None,
    ):
        super().__init__(parent)
        self._config = config
        self._storage_adapter = storage_adapter
        self._shutdown = False
        self._application_active = True

        self.setWindowTitle("ezdmb")
        self.setMinimumSize(0, 0)
        self._pageStack = QStackedWidget(self)
        self.setCentralWidget(self._pageStack)

        self.displayPage = android_display_page(
            config,
            self.showSettings,
            self._pageStack,
        )
        self.settingsPage = self._buildSettingsPage(config)
        self._pageStack.addWidget(self.displayPage)
        self._pageStack.addWidget(self.settingsPage)
        self._pageStack.setCurrentWidget(self.displayPage)

        app = QApplication.instance()
        if isinstance(app, QGuiApplication):
            app.applicationStateChanged.connect(
                self.onApplicationStateChanged
            )
            app.aboutToQuit.connect(self.shutdown)

        self.displayPage.display.resume()

    def _buildSettingsPage(self, config: configuration) -> QWidget:
        page = QWidget(self._pageStack)
        layout = QVBoxLayout(page)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        header = QHBoxLayout()
        self.backButton = QPushButton("Back to menu", page)
        self.backButton.setObjectName("androidBackButton")
        self.backButton.setMinimumHeight(48)
        self.backButton.clicked.connect(self.showMenu)
        header.addWidget(self.backButton)

        title = QLabel("Settings", page)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(title, 1)
        layout.addLayout(header)

        actions = QGridLayout()
        self.importBundleButton = QPushButton("Import Bundle", page)
        self.exportBundleButton = QPushButton("Export Bundle", page)
        self.importUrlButton = QPushButton("Import Bundle From URL", page)
        self.helpButton = QPushButton("Quickstart", page)
        self.aboutButton = QPushButton("About", page)
        action_buttons = (
            self.importBundleButton,
            self.exportBundleButton,
            self.importUrlButton,
            self.helpButton,
            self.aboutButton,
        )
        for button in action_buttons:
            button.setMinimumHeight(48)
            actions.addWidget(
                button,
                (action_buttons.index(button)) // 2,
                (action_buttons.index(button)) % 2,
            )
        self.importBundleButton.clicked.connect(self.importBundle)
        self.exportBundleButton.clicked.connect(self.exportBundle)
        self.importUrlButton.clicked.connect(self.importBundleFromUrl)
        self.helpButton.clicked.connect(self.showQuickstart)
        self.aboutButton.clicked.connect(self.showAbout)
        layout.addLayout(actions)

        self.settingsScrollArea = QScrollArea(page)
        self.settingsScrollArea.setWidgetResizable(True)
        QScroller.grabGesture(
            self.settingsScrollArea.viewport(),
            QScroller.ScrollerGestureType.TouchGesture,
        )
        self.configWidget = config_widget(
            None,
            config,
            android_mode=True,
            storage_adapter=self._storage_adapter,
        )
        self.settingsScrollArea.setWidget(self.configWidget)
        layout.addWidget(self.settingsScrollArea, 1)
        return page

    def showSettings(self):
        self.displayPage.display.pause()
        self._pageStack.setCurrentWidget(self.settingsPage)

    def showMenu(self):
        self._pageStack.setCurrentWidget(self.displayPage)
        if self._application_active:
            self.displayPage.display.resume()

    def onApplicationStateChanged(self, state):
        self._application_active = (
            state == Qt.ApplicationState.ApplicationActive
        )
        if (
            self._application_active
            and self._pageStack.currentWidget() is self.displayPage
        ):
            self.displayPage.display.resume()
        else:
            self.displayPage.display.pause()

    def importBundle(self):
        import_bundle(
            self.configWidget.trigger_settings_ui_update,
            self._config,
            storage_adapter=self._storage_adapter,
        )

    def exportBundle(self):
        export_bundle(
            self._config,
            storage_adapter=self._storage_adapter,
        )

    def importBundleFromUrl(self):
        import_bundle_from_url(
            self.configWidget.trigger_settings_ui_update,
            self._config,
        )

    def showQuickstart(self):
        QMessageBox.information(
            self,
            "Quickstart",
            "Add images, text, videos, or PDFs in Content. Choose an "
            "interval, None, or a schedule to control rotation. Changes "
            "are saved automatically.",
        )

    def showAbout(self):
        from ezdmb import __version__

        QMessageBox.information(
            self,
            "About ezdmb",
            f"ezdmb v{__version__}\n"
            "Digital menu board application.",
        )

    def keyPressEvent(self, event):
        if (
            event.key() in (Qt.Key.Key_Back, Qt.Key.Key_Escape)
            and self._pageStack.currentWidget() is self.settingsPage
        ):
            self.showMenu()
            event.accept()
            return
        super().keyPressEvent(event)

    def closeEvent(self, event):
        if self._pageStack.currentWidget() is self.settingsPage:
            self.showMenu()
            event.ignore()
            return
        self.shutdown()
        super().closeEvent(event)

    def shutdown(self):
        if self._shutdown:
            return
        self._shutdown = True
        self.displayPage.display.shutdown()
