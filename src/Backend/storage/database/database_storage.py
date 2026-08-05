from storage.storage import Storage

from .repositories.raw_repository import RawRepository
from .repositories.processed_repository import ProcessedRepository
#from .repositories.alarm_repository import AlarmRepository
#from .repositories.command_repository import CommandRepository
#from .repositories.log_repository import LogRepository


class DatabaseStorage(Storage):

    def __init__(self, session):

        self.raw_repository = RawRepository(session)

        self.processed_repository = ProcessedRepository(session)

        #self.alarm_repository = AlarmRepository(session)

        #self.command_repository = CommandRepository(session)

        #self.log_repository = LogRepository(session)


    def save_raw(self, data):

        return self.raw_repository.save(data)


    def save_processed(self, data):

        return self.processed_repository.save(data)


    def save_alarm(self, data):
        pass
        #return self.alarm_repository.save(data)


    def save_command(self, data):
        pass
        #return self.command_repository.save(data)


    def save_log(self, data):
        pass
        #return self.log_repository.save(data)