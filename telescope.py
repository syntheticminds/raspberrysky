import serial
import time

class Telescope:
    def __init__(self, debug=False):
        self.debug = debug
        self.mount = Mount(self)
        self.focuser = Focuser(self)
        self.clock = Clock(self)

    def connect(self, device):
        self.__serial_port = serial.Serial(
            port=device,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=5)

        # Check the telescope is listening.
        self.sendCommand(chr(0x06))

        response = self.__getCharacterResponse()

        if not response:
            raise Exception('Telescope did not reply.')

    def sendCommand(self, command, response_type='none'):
        if self.debug:
            print(command)

        self.__serial_port.write(command.encode('ascii'))

        if response_type == 'boolean':
            response = self.__getBooleanResponse()
        elif response_type == 'character':
            response = self.__getCharacterResponse()
        elif response_type == 'string':
            response = self.__getStringResponse()
        else:
            return

        return response

    def findHome(self):
        self.sendCommand(':hF#')

    def queryHomeStatus(self):
        home_status = self.sendCommand(':h?#', 'character')

        if (home_status == '1'):
            return 'found'
        elif (home_status == '2'):
            return 'in_progress'
        else:
            return 'failed'

    def setLocation(self):
        self.sendCommand(':W1#')

        self.sendCommand(':St+51*04#', 'boolean') # Latitude
        self.sendCommand(':Sg1*47#', 'boolean') # Longitude

    def __getCharacterResponse(self):
        character = self.__serial_port.read(1)

        if len(character) != 1:
            raise Exception('Timed out waiting for response.')

        return character.decode(errors='ignore')

    def __getBooleanResponse(self):
        character = self.__getCharacterResponse()

        if character == '1':
            return True
        else:
            return False

    def __getStringResponse(self):
        result = '';

        while True:
            character = self.__getCharacterResponse()

            if character == '#':
                break

            result += character

        return result

class Clock:
    def __init__(self, telescope):
        self.telescope = telescope

    def setTime(self):
        self.telescope.sendCommand(':hI' + time.strftime('%y%m%d%H%M%S') + '#', 'boolean')

    def getTime(self):
        time24 = self.telescope.sendCommand(':GL#', 'string')
        date = self.telescope.sendCommand(':GC#', 'string')

        return time.strptime(time24 + ' ' + date, '%H:%M:%S %m/%d/%y')

class Focuser:
    def __init__(self, telescope):
        self.telescope = telescope

    def focus(self, direction):
        if direction == 'in':
            self.telescope.sendCommand(':F+#')
        elif direction == 'out':
            self.telescope.sendCommand(':F-#')
        else:
            raise Exception('Unknown focus direction.')

    def setSpeed(self, speed):
        if speed == 'slowest' or speed == 1:
            self.telescope.sendCommand(':F1#')
        elif speed == 'slow' or speed == 2:
            self.telescope.sendCommand(':F2#')
        elif speed == 'fast' or speed == 3:
            self.telescope.sendCommand(':F3#')
        elif speed == 'fastest' or speed == 4:
            self.telescope.sendCommand(':F4#')
        else:
            raise Exception('Unknown focus speed.')

    def halt(self):
        self.telescope.sendCommand(':FQ#')

class Mount:
    def __init__(self, telescope):
        self.telescope = telescope

    def slew(self, direction):
        if direction == 'up':
            self.telescope.sendCommand(':Mn#')
        elif direction == 'down':
            self.telescope.sendCommand(':Ms#')
        elif direction == 'left':
            self.telescope.sendCommand(':Mw#')
        elif direction == 'right':
            self.telescope.sendCommand(':Me#')
        else:
            raise Exception('Unknown slew direction.')

    def setSpeed(self, speed):
        if speed == 'slowest' or speed == 1:
            self.telescope.sendCommand(':RG#')
        elif speed == 'slow' or speed == 2:
            self.telescope.sendCommand(':RC#')
        elif speed == 'fast' or speed == 3:
            self.telescope.sendCommand(':RM#')
        elif speed == 'fastest' or speed == 4:
            self.telescope.sendCommand(':RS#')
        else:
            raise Exception('Unknown slew speed.')

    def setHorizontalRate(self, rate):
        self.telescope.sendCommand(':RA' + str(rate * 8) + '#')

    def setVerticalRate(self, rate):
        self.telescope.sendCommand(':RE' + str(rate * 8) + '#')

    def halt(self, axis=None):
        if axis == 'x':
            self.telescope.sendCommand(':Qw#')
            self.telescope.sendCommand(':Qe#')
        elif axis == 'y':
            self.telescope.sendCommand(':Qn#')
            self.telescope.sendCommand(':Qs#')
        else:
            self.telescope.sendCommand(':Q#')