# Raspberry Sky
This is a personal project I've started to improve my knowledge of Python while making something interesting.

The motivation came after the original *Autostar II* handset packed up. It occured to me that I had everything I needed to make a PS3 controller wirelessly operate the telescope. Since the initial proof of concept, this script's features have been improved to enable basic calibration and GoTo functions.

## Requirements
* A Raspberry Pi
* A Meade LX200 telescope
* A USB to RS232 cable

A PS3 Sixaxis controller and bluetooth are required for manual control. A Raspberry Pi camera is required to take photos.

## Basic installation

    $ cd ~
    $ sudo apt-get install git -y
    $ git clone http://www.github.com/syntheticminds/raspberrysky
    $ cd raspberrysky
    $ pip install

### Controller support

    $ sudo apt-get install pi-bluetooth libusb-dev -y

Next, we need a utility that will allow us to pair a PS3 controller with the Pi. At this stage, be sure the controller is plugged into the Pi via USB.

    $ wget http://www.pabr.org/sixlinux/sixpair.c
    $ gcc -o sixpair sixpair.c -lusb
    $ sudo ~/sixpair

With the controller disconnected and powered off, run the following commands.

    $ sudo bluetoothctl
    discoverable on
    agent on

Power-on the controller and it should start talking to the Pi. Copy the MAC address; we'll need it. Enter:

    connect [MAC address]

Try the above command again and again if it says *not available*. If it says *Failed to connect* then it has worked. Now we make our changes permanent.

    trust [MAC address]
    quit

TODO: Controller configuration in settings.yaml

## Configuration
We use a settings file to tell the script where to look for devices.

    $ cd raspberrysky
    $ cp settings.yaml.example settings.yaml

    $ python3 RaspberrySky.py

## Manual controls
The left thumbstick slews the telescope. How far you push the stick determins how fast it slews. The right thumbstick makes small adjustments - ideal for finding and positioning objects in the eyepiece. The left and right triggers focus out and in respectively.

TODO: Camera configuration in settings.yaml
