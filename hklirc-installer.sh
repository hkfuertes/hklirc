#!/bin/bash

# Check for SU
if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

# Installing git
tput setaf 2; echo "[+] Installing git";tput setaf 7;
apt install -y git

# Clonning the project
tput setaf 2; echo "[+] Cloning the project";tput setaf 7;
git clone https://github.com/hkfuertes/hklirc

# Accessing the project
cd hklirc

#Installing the USB-Gadget
tput setaf 2; echo "[+] Installing USB-Gadget";tput setaf 7;
cd gadget
chmod +x ./usb-gadget-install.sh
./usb-gadget-install.sh
cd ..

# Installing the python daemon
tput setaf 2; echo "[+] Installing the python daemon";tput setaf 7;
cd daemon_python
chmod +x ./install_daemon.sh
./install_daemon.sh
cd ..

# Installing the django server
tput setaf 2; echo "[+] Installing the django server";tput setaf 7;
cd server
chmod +x ./install_server.sh
./install_server.sh
cd ..

# Changing permission for the folder
tput setaf 2; echo "[+] Changing permission for the folder...";tput setaf 7;
chmod 777 -R hklirc

# Installed, rebooting
tput setaf 2; echo "[+] Installed, rebooting...";tput setaf 7;
reboot