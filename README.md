# Raspberry Sky
This is a personal project I've started to improve my knowledge of Python while making something interesting.

The aim is to make the telescope I have inherited steerable via a PS3 controller. The original *Autostar II* handset it came with packed up and sadly the telescope has been gathering dust ever since. Now, with the help of a Raspberry Pi and a serial connection, the telescope has been revived.

## Requirements
* A Raspberry Pi with WiFi and Bluetooth.
* A PS3 Sixaxis Controller
* A Meade LX200 telescope
* USB to RS232 cable
* Mini to standard USB cable

## Installation
These instructions are for a fresh Rasbian Lite image. Dip in where you need to.

    $ sudo apt-get update
    $ sudo apt-get dist-upgrade

### Set up WiFi

    $ sudo nano /etc/wpa_supplicant/wpa_supplicant.conf

Add the following lines to the file:

    network={
        ssid="Access Point Name"
        psk="access_point_password"
    }

#### Disable wireless power saving
    
    $ sudo nano /etc/network/interfaces

Add the line `wireless-power off` to the end of the file.

### Raspberry Pi configuration

    $ sudo raspi-config

Enable the camera and expand the file system. When prompted, reboot the Pi.

### Installing code and dependencies

    $ sudo apt-get install python3-pip -y
    $ sudo apt-get install git -y

    $ sudo pip3 install picamera
    $ sudo pip3 install evdev
    $ sudo pip3 install pyserial
    $ sudo pip3 install pyyaml --global-option="--without-libyaml"

    $ git clone http://www.github.com/syntheticminds/raspberrysky

### Pairing the controller

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

## Configuration
We use a settings file to tell the script where to look for devices.

    $ cd raspberrysky
    $ cp settings.yaml.example settings.yaml

    $ python3 RaspberrySky.py
    
## Controls
The left thumbstick slews the telescope. How far you push the stick determins how fast it slews. The Right thumbstick makes small adjustments - ideal for finding and positioning objects in the eyepiece. The left and right triggers focus out and in respectively.

Pressing X will take a photo if the Raspberry Pi camera is attached. Further integration of the camera is work in progress.