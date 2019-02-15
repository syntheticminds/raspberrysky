import evdev
from threading import Thread
import time

import sys

# invert_left = settings['controller']['left_thumbstick']['invert_y']
# reverse_right = settings['controller']['right_thumbstick']['reverse']

class Controller(Thread):
    def __init__(self, settings):
        super(Controller, self).__init__()

        self.daemon = True

        self.__device = settings['device']

        self.buttons = {
            'x': Button(),
            'l3': Button(),
            'r3': Button()
        }

        self.thumbsticks = {
            'left': Thumbstick(),
            'right': Thumbstick()
        }

        self.triggers = {
            'left': Trigger(),
            'right': Trigger()
        }

    def connect(self):
        if self.__device.name not in ('Sony PLAYSTATION(R)3 Controller', 'Sony Computer Entertainment Wireless Controller'):
            raise Exception('This is not a PS3 controller.')

        self.start()

    def run(self):
        for event in self.__device.read_loop():
            # Buttons
            if event.type == 1:
                if event.code == 302:
                    self.buttons['x'].update(event)
                    continue
                if event.code == 289:
                    self.buttons['l3'].update(event)
                    continue
                if event.code == 290:
                    self.buttons['r3'].update(event)
                    continue
            elif event.type == 3:
                # Thumbsticks
                if event.code == 0:
                    self.thumbsticks['left'].updateX(event)
                    continue
                elif event.code == 1:
                    self.thumbsticks['left'].updateY(event)
                    continue
                elif event.code == 2:
                    self.thumbsticks['right'].updateX(event)
                    continue
                elif event.code == 5:
                    self.thumbsticks['right'].updateY(event)
                    continue

                # Triggers
                if event.code == 48:
                    self.triggers['left'].update(event)
                    continue
                elif event.code == 49:
                    self.triggers['right'].update(event)
                    continue

class Button:
    def __init__(self):
        self.__pressed = False

    def update(self, event):
        if event.value == 1:
            self.__pressed = True

    def wasPressed(self):
        if self.__pressed:
            self.__pressed = False

            return True
        else:
            return False

class Thumbstick:
    def __init__(self):
        self.__position_x = 0
        self.__position_y = 0

    def updateX(self, event):
        self.__position_x = self.__normalisePosition(event.value)

    def updateY(self, event):
        self.__position_y = self.__normalisePosition(event.value)

    def getXPosition(self):
        return self.__position_x

    def getYPosition(self):
        return self.__position_y * -1 # We want positive values to mean up, like Cartesian coordinates

    def __normalisePosition(self, position):
        normalised = (position - 128) / 128

        if abs(normalised) > 0.15:
            return normalised
        else:
            return 0

class Trigger:
    def __init__(self):
        self.__position = 0

    def update(self, event):
        self.__position = event.value

    def getPosition(self):
        return self.__position / 255
