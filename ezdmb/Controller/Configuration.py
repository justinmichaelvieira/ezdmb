import os
import errno
import json

# Encapsulates configuration file serialization and deserialization
class Configuration(object):

    ##############################
    # Properties
    ##############################

    def set_data(self, value):
        self._data = value

    def get_data(self):
        return self._data

    Data = property(get_data, set_data)

    def set_use_images(self, value):
        self._use_images = value

    def get_use_images(self):
        return self._use_images

    UseImages = property(get_use_images, set_use_images)

    def set_use_html(self, value):
        self._use_html = value

    def get_use_html(self):
        return self._use_html

    UseHTML = property(get_use_html, set_use_html)

    def set_use_imported(self, value):
        self._use_imported = value

    def get_use_imported(self):
        return self._use_imported

    UseImported = property(get_use_imported, set_use_imported)

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

    def set_content_array(self, value):
        self._content_array = value

    def get_content_array(self):
        return self._content_array

    ContentArray = property(get_content_array, set_content_array)

    ##############################
    # Functions
    ##############################

    # Initializes the object when Configuration is first instanced
    def __init__(self):
        super(self.__class__, self).__init__()
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        self._data = dict()
        self._configPath = "dmb_config.json"
        # Create config file if it does not already exist
        if not os.path.exists(self._configPath):
            try:
                file_handle = os.open(self._configPath, flags)
            except OSError as e:
                if e.errno == errno.EEXIST:  # Failed as the file already exists.
                    pass
                else:  # Something unexpected went wrong so reraise the exception.
                    raise
            else:  # No exception, so the file must have been created successfully.
                with os.fdopen(file_handle, "a") as file_obj:
                    # Settings defaults here, for first runs
                    self.SaveConfig(True, False, False, True, "0.5", [f'{os.getcwd()}/ezdmb/Images/354580462_orig.jpg'])

        with open(self._configPath, "r+") as json_data_file:
            self._data = json.load(json_data_file)

        # Set variables for the app to use
        self.set_use_images(self._data["use_images"])
        self.set_use_html(self._data["use_html"])
        self.set_use_imported(self._data["use_imported"])
        self.set_rotate_content(self._data["rotate_content"])
        self.set_rotate_content_time(float(self._data["rotate_content_time"]))
        self.set_content_array(self._data["imported_content"])

    # Saves our JSON config file
    def SaveConfig(
        self,
        UseImages,
        UseHTML,
        UseImported,
        RotateContent,
        RotateContentTime,
        ContentArray,
    ):
        self._data["use_images"] = UseImages
        self._data["use_html"] = UseHTML
        self._data["use_imported"] = UseImported
        self._data["rotate_content"] = RotateContent
        self._data["rotate_content_time"] = float(RotateContentTime)
        self._data["imported_content"] = ContentArray
        with open(self._configPath, "w+") as outfile:
            json.dump(self.get_data(), outfile)
