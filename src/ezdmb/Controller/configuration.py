"""
configuration.py
Encapsulates configuration file serialization and deserialization.
"""

import errno
import json
import os

from PySide6.QtCore import QObject, Signal

from ezdmb.Utility.path_utility import get_appdata_path


def default_time_blocks():
    return {
        "repeat": "None",
        "daily": [],
        "weekly": {},
        "dated": {},
    }


def default_content_groups(content_array=None):
    return [
        {
            "id": "default",
            "name": "Default",
            "content": list(content_array or []),
        }
    ]


# pylint: disable=too-many-instance-attributes, missing-function-docstring, missing-class-docstring
class configuration(QObject):
    # signals
    configUpdated = Signal(dict)

    # properties
    def set_data(self, value):
        self._data = value

    def get_data(self):
        return self._data

    Data = property(get_data, set_data)

    def set_rotate_content(self, value):
        self._rotate_content = value

    def get_rotate_content(self):
        return self._rotate_content

    RotateContent = property(get_rotate_content, set_rotate_content)

    def set_rotate_content_time(self, value):
        self._rotate_content_time = value

    def get_rotate_content_time(self):
        return self._rotate_content_time

    RotateContentTime = property(get_rotate_content_time, set_rotate_content_time)

    def set_rotation_mode(self, value):
        self._rotation_mode = value

    def get_rotation_mode(self):
        return self._rotation_mode

    RotationMode = property(get_rotation_mode, set_rotation_mode)

    def set_content_array(self, value):
        self._content_array = value

    def get_content_array(self):
        return self._content_array

    ContentArray = property(get_content_array, set_content_array)

    def set_time_blocks(self, value):
        self._time_blocks = value

    def get_time_blocks(self):
        return self._time_blocks

    TimeBlocks = property(get_time_blocks, set_time_blocks)

    def set_content_groups(self, value):
        self._content_groups = value

    def get_content_groups(self):
        return self._content_groups

    ContentGroups = property(get_content_groups, set_content_groups)

    def get_config_path(self):
        return self.config_path

    def set_config_path(self, value):
        self.config_path = value

    ConfigPath = property(get_config_path, set_config_path)

    # Functions

    # Initializes the object when Configuration is first instanced

    def __init__(self):
        super(self.__class__, self).__init__()
        # self._logger = logger

        flags = os.O_CREAT | os.O_RDWR
        self._data = {}

        appdata_path = get_appdata_path()

        # self._logger.info(f"Configuration path: {appdata_path}")

        # Create appdata directory if it does not already exist
        os.makedirs(appdata_path, exist_ok=True)

        self.config_path = os.path.join(appdata_path, "dmb_config.json")
        # Create config file if it does not already exist
        if not os.path.exists(self.config_path):
            try:
                os.open(self.config_path, flags)
            except OSError as e:
                if e.errno == errno.EEXIST:  # Failed as the file already exists.
                    pass
                else:  # Something unexpected went wrong so reraise the exception.
                    raise
            else:  # No exception, so the file must have been created successfully.
                # Settings defaults here, for first runs
                self.save_config(
                    True,
                    "15",
                    [],
                    TimeBlocks=default_time_blocks(),
                    ContentGroups=default_content_groups(),
                    RotationMode="interval",
                )

        self.load_from_file(self.config_path)

    def load_from_file(self, path):
        with open(path, "r+") as json_data_file:
            self._data = json.load(json_data_file)

        if "content_groups" not in self._data:
            self._data["content_groups"] = default_content_groups(
                self._data.get("imported_content", [])
            )
        elif not self._data["content_groups"]:
            self._data["content_groups"] = default_content_groups()

        for index, group in enumerate(self._data["content_groups"]):
            group.setdefault("id", f"group-{index + 1}")
            group.setdefault("name", f"Group {index + 1}")
            group.setdefault("content", [])

        self._data["imported_content"] = [
            content
            for group in self._data["content_groups"]
            for content in group["content"]
        ]

        self._data.setdefault("time_blocks", default_time_blocks())
        first_group_id = self._data["content_groups"][0]["id"]
        time_blocks = self._data["time_blocks"]
        for block in time_blocks["daily"]:
            block.setdefault("group_id", first_group_id)
        for day_blocks in time_blocks["weekly"].values():
            for block in day_blocks:
                block.setdefault("group_id", first_group_id)
        for date_blocks in time_blocks["dated"].values():
            for block in date_blocks:
                block.setdefault("group_id", first_group_id)

        rotation_mode = self._data.get("rotation_mode")
        if rotation_mode is None:
            rotation_mode = (
                "interval" if self._data.get("rotate_content", True) else "none"
            )
        if rotation_mode not in ("interval", "schedule", "none"):
            raise ValueError(f"Unsupported rotation mode: {rotation_mode}")
        self._data["rotation_mode"] = rotation_mode
        self._data["rotate_content"] = rotation_mode == "interval"

        # Set variables for the app to use
        self.set_rotate_content(rotation_mode == "interval")
        self.set_rotate_content_time(int(self._data["rotate_content_time"]))
        self.set_content_array(self._data["imported_content"])
        self.set_time_blocks(self._data["time_blocks"])
        self.set_rotation_mode(rotation_mode)
        self.set_content_groups(self._data["content_groups"])

    # Saves our JSON config file
    def save_config(
        self,
        RotateContent,
        RotateContentTime,
        ContentArray,
        savePath=None,
        TimeBlocks=None,
        ContentGroups=None,
        RotationMode=None,
    ):
        self._data["rotate_content_time"] = int(RotateContentTime)
        if ContentGroups is None:
            ContentGroups = default_content_groups(ContentArray)
        if not ContentGroups:
            raise ValueError("At least one content group is required.")
        ContentArray = [
            content
            for group in ContentGroups
            for content in group["content"]
        ]

        if RotationMode is None:
            RotationMode = "interval" if RotateContent else "none"
        if RotationMode not in ("interval", "schedule", "none"):
            raise ValueError(f"Unsupported rotation mode: {RotationMode}")

        self._data["rotation_mode"] = RotationMode
        self._data["rotate_content"] = RotationMode == "interval"
        self._data["imported_content"] = ContentArray
        self._data["content_groups"] = ContentGroups
        self.set_rotate_content(RotationMode == "interval")
        self.set_rotation_mode(RotationMode)
        self.set_content_array(ContentArray)
        self.set_content_groups(ContentGroups)

        if TimeBlocks is None:
            TimeBlocks = self._data.get("time_blocks", default_time_blocks())
        self._data["time_blocks"] = TimeBlocks
        self.set_time_blocks(TimeBlocks)

        if savePath is None:  # Default to the config path if not doing a save as
            savePath = self.config_path
        with open(savePath, "w+") as outfile:
            json.dump(self._data, outfile)

        self.configUpdated.emit(self._data)
