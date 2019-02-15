from threading import Thread

class Console(Thread):
    def __init__(self, telescope, sky):
        super(Console, self).__init__()
        
        self.daemon = True

        self.__command = None

        self.start()

    def run(self):
        while True:
            if self.__command is None:
                command = input('Enter a command: ')

                self.__command = command.lower()

    def getCommand(self):
        command = self.__command

        self.__command = None

        return command