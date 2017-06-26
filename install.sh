#!/bin/sh

# Update packages
sudo apt-get update
sudo apt-get dist-upgrade

# Disable Wi-Fi power saving
sudo echo "wireless-power off" >> /etc/network/interfaces

# Install pip
sudo apt-get install python3-pip -y

# Install dependencies
sudo pip3 install picamera
sudo pip3 install evdev
sudo pip3 install pyserial
sudo pip3 install pyyaml --global-option="--without-libyaml"
sudo pip3 install ephem
