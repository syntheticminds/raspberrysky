import os
import picamera
import socket
import time

class Camera():
    def __init__(self):
        self.__camera = picamera.PiCamera()
        self.__photo_directory = os.path.dirname(os.path.realpath(__file__)) + '/photos/'

    def takePhoto(self):
        file_name = 'raspberrysky' + time.strftime('%y-%m-%d_%H:%M:%S') + '.jpg'

        try:
            self.__camera.resolution = (1024, 768)
            time.sleep(2)
            self.__camera.capture(output=self.__photo_directory + file_name)

            return file_name
        except:
            return False