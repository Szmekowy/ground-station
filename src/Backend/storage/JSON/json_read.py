import json

class JsonReader:
    def __init__(self):
        pass
    def read_all(self, path):
        data = []
  
        with open(path, "r") as file:

            for line in file:
                data.append(
                    json.loads(line)
                )

        return data

    def read_last(self, path):

        last = None

        with open(path, "r") as file:

            for line in file:
                last = json.loads(line)

        return last

    def read_last_n(self, path, n):

        with open(path, "r") as file:

            lines = file.readlines()

        return [
            json.loads(line)
            for line in lines[-n:]
        ]