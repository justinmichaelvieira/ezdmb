import json

class MenuDataImport:
    def loadImportData(self):
        with open("menu.json", 'r+') as json_data_file:
            self._data = json.load(json_data_file)