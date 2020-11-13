import json

class TableWithJson:
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        try:
            with open(self.filename, 'r') as f:
                obj = f.read().strip("'<>() ").replace('\'', '\"')
                self.data = json.loads(obj)
        except Exception as e:
            print(e)
        return self.data

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_value(self, key):
        return self.data[key]

    def increse(self, key, value):
        self.data[key] += value
    
    def reset(self, key, value):
        self.data[key] = value

    def write_data(self):
        with open(self.filename, "w") as write_file:
            json.dump(self.data, write_file)
