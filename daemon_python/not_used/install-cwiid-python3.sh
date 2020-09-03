#!/bin/bash

sudo apt install bison flex automake libbluetooth-dev

git clone https://github.com/azzra/python3-wiimote
cd python3-wiimote

aclocal
autoconf
./configure
make
sudo make install