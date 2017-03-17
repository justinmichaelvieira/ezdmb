import sys,os
import errno
import json
from PyQt5.QtCore import QStandardPaths

# Encapsulates configuration file serialization and deserialization
class Configuration(object):

    ##############################
    # Properties
    ##############################

    # Defines a SavedImage "property" for use by other classes
    def set_savedImage(self, value):
        self._savedImage = value
    def get_savedImage(self):
        return self._savedImage
    SavedImage = property(get_savedImage, set_savedImage)

    # Defines a Data "property" for use by other classes
    def set_data(self, value):
        self._data = value
    def get_data(self):
        return self._data
    Data = property(get_data, set_data)

    ##############################
    # Functions
    ##############################

    # Initializes the object when Configuration is first instanced
    def __init__(self):
        super(self.__class__, self).__init__()
        #private vars
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        self._data = dict()
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
                    self.SaveConfig(QStandardPaths.writableLocation(QStandardPaths.HomeLocation) + self._savedImage)
                    #json.dump(self.get_data(), file_obj)

        with open(self._configPath, 'r+') as json_data_file:
            self._data = json.load(json_data_file)
        # Set variables for the app to use
        print(self._data['saved_image'])
        self.set_savedImage(self._data['saved_image'])
        self._advancedMode = False
        self._advancedFiles = [0]
        self._timeout = 120

    # Saves our JSON config file
    def SaveConfig(self, NewImage):
        self._data['saved_image'] = NewImage
        with open(self._configPath, 'w+') as outfile:
            json.dump(self.get_data(), outfile)

    # Save text file to be rendered under a header
    def SaveTextFile(self, fileContents):
        textFile= open(QStandardPaths.writableLocation(QStandardPaths.HomeLocation) + "/menu.txt","w")
        textFile.write(fileContents)
        textFile.close()