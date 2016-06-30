#!/bin/bash
sudo apt install python3-pip python-pip -y
sudo pip3 install python-telegram-bot
sudo pip3 install -U urllib3
sudo pip3 install sounddevice pyaudio
cd /tmp
git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
cd ffmpeg
./configure
make
sudo make install
