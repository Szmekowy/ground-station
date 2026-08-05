import os
import json

from storage.storage import Storage

from .paths import RAW_DATA_FILE
from .paths import PROCESSED_DATA_FILE
from .paths import ALARMS_FILE
from .paths import COMMANDS_FILE
from .paths import LOGS_FILE

class JsonStorage(Storage):
    def __init__(self):
        pass

    def _save(self, data, path):

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        with open(path, "a") as file:
            file.write(
                json.dumps(data) + "\n"
            )

    def save_raw(self, data):

        self._save(
            data,
            RAW_DATA_FILE
        )
    def save_processed(self, data):

        self._save(
            data,
            PROCESSED_DATA_FILE
        )
    def save_alarm(self, data):

        self._save(
            data,
            ALARMS_FILE
        )
    def save_command(self, data):

        self._save(
            data,
            COMMANDS_FILE
        )
    def save_log(self, data):

        self._save(
            data,
            LOGS_FILE
        )