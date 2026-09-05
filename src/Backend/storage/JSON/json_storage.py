import os
import json

from storage.storage import Storage

from src.config.backend_json import JSON_PATHS as PATHS

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
            PATHS.RAW_DATA_FILE
        )
    def save_processed(self, data):

        self._save(
            data,
            PATHS.PROCESSED_DATA_FILE
        )
    def save_alarm(self, data):

        self._save(
            data,
            PATHS.ALARMS_FILE
        )
    def save_command(self, data):

        self._save(
            data,
            PATHS.COMMANDS_FILE
        )
    def save_log(self, data):

        self._save(
            data,
            PATHS.LOGS_FILE
        )