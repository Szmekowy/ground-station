class Storage:

    def save_raw(self, data):
        raise NotImplementedError


    def save_processed(self, data):
        raise NotImplementedError


    def save_alarm(self, data):
        raise NotImplementedError


    def save_command(self, data):
        raise NotImplementedError


    def save_log(self, data):
        raise NotImplementedError