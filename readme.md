# hkLirc
This is a simple project for a Raspberry Pi that aims to bridge the **gpio-ir** interface with a **HID device**.

There are 3 parts to the project, the [gadget](gadget) configuration part, the [server](server) to manage the mappings and the actual python [daemon](daemon_python) that will trigger the actual keystrokes in the connected PC.

## Requirements
To install the project a blank RaspberryPiOS image is required. _Unfortunatelly the usb-ethernet (RNDIS) driver is not working for the 64bit OS._
  > You can find it here: https://www.raspberrypi.org/downloads/raspberry-pi-os/

The system expects the TSOP4838 to be connected in **PIN 14**, it can be changed after install by editing `/boot/config.txt`.

## Installation
`wget -O - https://raw.githubusercontent.com/hkfuertes/hklirc/master/hklirc-installer.sh | sudo bash`

