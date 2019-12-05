command_list = []
admin_command_list = []


class Command:
    def __init__(self):
        self.__keys = []
        self.description = ''
        command_list.append(self)

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, mas):
        for k in mas:
            self.__keys.append(k.lower())

    def process(self):
        pass


class AdminCommand:
    def __init__(self):
        self.__keys = []
        self.description = ''
        admin_command_list.append(self)

    @property
    def keys(self):
        return self.__keys

    @keys.setter
    def keys(self, mas):
        for k in mas:
            self.__keys.append(k.lower())

    def process(self):
        pass
