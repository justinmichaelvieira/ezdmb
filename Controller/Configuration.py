import sys,os
import errno
import json
from PyQt5.QtCore import QStandardPaths

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

    def set_savedImage(self, value):
        self._savedImage = value
    def get_savedImage(self):
        return self._savedImage
    SavedImage = property(get_savedImage, set_savedImage)

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
        #private vars
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        self._data = dict()
        #defaults here, for first runs
        self._savedImage = "default.jpg"
        self._configPath = QStandardPaths.writableLocation(QStandardPaths.HomeLocation) + "/dmb_config.json"
        #create config file if it does not already exist
        if not os.path.exists(self._configPath):
            try:
                file_handle = os.open(self._configPath, flags)
            except OSError as e:
                if e.errno == errno.EEXIST:  # Failed as the file already exists.
                    pass
                else:  # Something unexpected went wrong so reraise the exception.
                    raise
            else:  # No exception, so the file must have been created successfully.
                with os.fdopen(file_handle, 'a') as file_obj:
                # Using `os.fdopen` converts the handle to an object that acts like a
                # regular Python file object, and the `with` context manager means the
                # file will be automatically closed when we're done with it.
                    self.SaveConfig(QStandardPaths.writableLocation(QStandardPaths.HomeLocation) + self._savedImage, True, True, True, True, "0.5", [])
                    #json.dump(self.get_data(), file_obj)

        with open(self._configPath, 'r+') as json_data_file:
            self._data = json.load(json_data_file)
        # Set variables for the app to use
        self.set_savedImage(self._data['saved_image'])
        self.set_use_images(self._data['use_images'])
        self.set_use_html(self._data['use_html'])
        self.set_use_imported(self._data['saved_image'])
        self.set_rotate_content(self._data['rotate_content'])
        self.set_rotate_content_time(float(self._data['rotate_content_time']))
        self.set_content_array (self._data['imported_content'])

    def SaveNewImage(self, NewImage):
        self.SaveConfig(NewImage, self.UseImages, self.UseHTML, self.UseImported, self.RotateContent, self.RotateContentTime, self.ContentArray)

    def SaveSettings(self, UseImages, UseHTML, UseImported, RotateImages, RotateImagesTime, ImageArray):
        self.SaveConfig(self._savedImage, UseImages, UseHTML, UseImported, RotateImages, RotateImagesTime, ImageArray)

    # Saves our JSON config file
    def SaveConfig(self, NewImage, UseImages, UseHTML, UseImported, RotateContent, RotateContentTime, ContentArray):
        self._data['saved_image'] = NewImage
        self._data['use_images'] = UseImages
        self._data['use_html'] = UseHTML
        self._data['use_imported'] = UseImported
        self._data['rotate_content'] = RotateContent
        self._data['rotate_content_time'] = float(RotateContentTime)
        self._data['imported_content'] = ContentArray
        with open(self._configPath, 'w+') as outfile:
            json.dump(self.get_data(), outfile)

    # Save text file to be rendered under a header
    def SaveTextFile(self, fileContents):
        textFile= open(QStandardPaths.writableLocation(QStandardPaths.HomeLocation) + "/menu.txt","w")
        textFile.write(fileContents)
        textFile.close()