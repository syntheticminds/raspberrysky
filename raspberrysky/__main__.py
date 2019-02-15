import sys
import time
import yaml

from camera import Camera
from console import Console
from controller import Controller
from sky import Sky
from telescope import Telescope

# Load settings
settings = yaml.load(open('settings.yaml', 'r'))

# Prepare the sky
sky = Sky(settings['site'])

# Connect to the telescope
telescope = Telescope(settings['telescope'])
telescope.connect()

# Start listening to the console
console = Console(telescope, sky)

# Set up controller
if settings['controller']['enabled']:
    controller = Controller(settings['controller'])
    controller.connect()
else:
    controller = None

# Set up camera
if settings['camera']['enabled']:
    camera = Camera()
else
    camera = None

# Start checking for events
while True:
    command = console.getCommand()

    if command:
        if command in ('quit', 'exit'):
            sys.exit()
        elif command == 'calibrate':
            telescope.calibrate()
        elif command == 'take photo':
            if camera is not None: camera.takePhoto()
        elif command.startswith('point at '):
            target = command[len('point at '):]

            if target == 'polaris':
                coordinates = sky.findStar(11767);

                telescope.mount.slewTo(coordinates)
            elif target in ('moon', 'the moon'):
                coordinates = sky.findPlanet('moon');

                telescope.mount.slewTo(coordinates)
            elif target in ('sun', 'the sun'):
                coordinates = sky.findPlanet('sun');

                telescope.mount.slewTo(coordinates)
            else:
                print('Unknown target')
        else:
            print('Unknown command')

    if controller is not None:
        # SETTINGS
        if controller.buttons['l3'].wasPressed():
            invert_left = not invert_left

        if controller.buttons['r3'].wasPressed():
            reverse_right = not reverse_right

        # FINDING
        right_x_axis = controller.thumbsticks['right'].getXPosition()
        right_y_axis = controller.thumbsticks['right'].getYPosition()

        if abs(right_x_axis) > 0 or abs(right_y_axis) > 0:
            if abs(right_x_axis) > 0.25 or abs(right_y_axis) > 0.25:
                telescope.mount.setSpeed('slowest')
            if abs(right_x_axis) > 0.5 or abs(right_y_axis) > 0.5:
                telescope.mount.setSpeed('slow')
            if abs(right_x_axis) > 0.75 or abs(right_y_axis) > 0.75:
                telescope.mount.setSpeed('fast')

            if (not reverse_right and right_x_axis < 0) or (reverse_right and right_x_axis > 0):
                telescope.mount.slew('right')
            elif (not reverse_right and right_x_axis > 0) or (reverse_right and right_x_axis < 0):
                telescope.mount.slew('left')
            else:
                telescope.mount.halt('x')

            if (not reverse_right and right_y_axis > 0) or (reverse_right and right_y_axis < 0):
                telescope.mount.slew('up')
            elif (not reverse_right and right_y_axis < 0) or (reverse_right and right_y_axis > 0):
                telescope.mount.slew('down')
            else:
                telescope.mount.halt('y')
        else:
            # SLEWING
            left_x_axis = controller.thumbsticks['left'].getXPosition()
            left_y_axis = controller.thumbsticks['left'].getYPosition()

            if abs(left_x_axis) > 0:
                telescope.mount.setHorizontalRate(abs(left_x_axis))

                if left_x_axis < 0:
                    telescope.mount.slew('left')
                else:
                    telescope.mount.slew('right')
            else:
                telescope.mount.halt('x')

            if abs(left_y_axis) > 0:
                telescope.mount.setVerticalRate(abs(left_y_axis))

                if (not invert_left and left_y_axis > 0) or (invert_left and left_y_axis < 0):
                    telescope.mount.slew('up')
                else:
                    telescope.mount.slew('down')
            else:
                telescope.mount.halt('y')

            # FOCUSING
            left_trigger = controller.triggers['left'].getPosition()
            right_trigger = controller.triggers['right'].getPosition()

            focus = right_trigger - left_trigger
            focus_speed = floor(abs(focus) / 0.25)

            if focus_speed > 0:
                telescope.focuser.setSpeed(focus_speed)

                if focus > 0:
                    telescope.focuser.focus('in')
                else:
                    telescope.focuser.focus('out')
            else:
                telescope.focuser.halt()

        # PHOTO        
        if controller.buttons['x'].wasPressed():
            if camera is not None: camera.takePhoto()

    time.sleep(0.1)
