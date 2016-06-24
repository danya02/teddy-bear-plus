#!/bin/bash
sudo apt install libreadline-dev libssl-dev lua5.2 liblua5.2-dev libevent-dev libjansson-dev libpython-dev make python3-pip -y
cd /tmp
git clone --recursive https://github.com/vysheng/tg.git
cd tg
./configure --disable-libconfig
make
mkdir ~/.teddy_bear_plus
cp ./bin/telegram-cli ~/.teddy_bear_plus/telegram-cli
cd /tmp
git clone --recursive https://github.com/luckydonald/pytg
sudo pip install pip-utils
sudo pip install pytg
sudo pip3 install pip3-utils
sudo pip3 install pytg

