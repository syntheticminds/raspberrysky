from threading import Thread
import sys

class Console(Thread):
    def __init__(self, telescope, sky):
        super(Console, self).__init__()

        self.__telescope = telescope
        self.__sky = sky

        self.start()

    def run(self):
        while True:
            command = input('Enter a command: ')

            if command in ('quit', 'exit'):
                sys.exit()
            elif command == 'telescope.findHome':
                telescope.findHome()
            elif command.startswith('telescope.mount.slewTo'):
                argument = command.split(' ', 1)[1]
                coordinates = [float(i) for i in argument.split(',', 1)]

                self.__telescope.mount.slewTo(coordinates)
            elif command == 'goto Polaris':
                coordinates = self.__sky.whereIsPolaris();

                self.__telescope.mount.slewTo(coordinates)
            elif command == 'goto the Moon':
                coordinates = self.__sky.whereIsTheMoon();

                self.__telescope.mount.slewTo(coordinates)
            elif command == 'goto the Sun':
                coordinates = self.__sky.whereIsTheSun();

                self.__telescope.mount.slewTo(coordinates)
            else:
                print('Unknown command')
