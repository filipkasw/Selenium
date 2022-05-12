import json
import os


class ReadJson():

    def __init__(self, file_name):
        script_dir = os.path.dirname(__file__)
        self.abs_file_path = os.path.join(script_dir, file_name)

    def get_value(self, value):
        with open(self.abs_file_path, 'r') as data:
            obj = data.read()
        object = json.loads(obj)
        return object[value]

    def set_value(self, object, value):
        with open(self.abs_file_path, 'r') as jsonFile:
            read_data = json.load(jsonFile)
        read_data[object] = value
        with open(self.abs_file_path, 'w') as data:
            json.dump(read_data, data, indent=4)

        
