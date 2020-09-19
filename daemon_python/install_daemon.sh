#!/bin/bash

# Check for SU
if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

# Installing Lirc
tput setaf 2; echo "[+] Installing Lirc";tput setaf 7;
apt install -y lirc

DRIVER="default"
DEVICE="/dev/lirc0"
DEFAULT_REMOTE="https://sourceforge.net/p/lirc-remotes/code/ci/master/tree/remotes/sony/SCPH-10150.lircd.conf?format=raw"
DEFAULT_REMOTE_NAME="SCPH-10150.lircd.conf"
DEFAULT_PATH="/home/pi/hklirc/daemon_python"

# Changing lirc_options.conf
tput setaf 2; echo "[+] Changing lirc_options.conf";tput setaf 7;
sed -i "s/^\(driver\s*=\s*\).*\$/\1$DRIVER/" /etc/lirc/lirc_options.conf
sed -i "s/^\(device\s*=\s*\).*\$/\1$DEVICE/" /etc/lirc/lirc_options.conf

# Adding pin configs to /boot/config.txt
tput setaf 2; echo "[+] Adding pin configs to /boot/config.txt";tput setaf 7;
echo "dtoverlay=gpio-ir,gpio_pin=14" | tee -a /boot/config.txt

# Hiding default config
tput setaf 2; echo "[+] Hiding default config";tput setaf 7;
mv devinput.lircd.conf devinput.lircd.conf.bak

# Downloading example remote
tput setaf 2; echo "[+] Donwloading example remote: $DEFAULT_REMOTE_NAME";tput setaf 7;
wget $DEFAULT_REMOTE -O "/etc/lirc/lircd.conf.d/$DEFAULT_REMOTE_NAME"

# Installing service
tput setaf 2; echo "[+] Installing and enabling service";tput setaf 7;
sed -i "s|$DEFAULT_PATH|$(pwd)|g" hklircd.service
cp hklircd.service /etc/systemd/system/
systemctl enable hklircd.service

# Creating launcher
tput setaf 2; echo "[+] Creating launcher";tput setaf 7;
echo "#!/bin/bash" > hklircd.sh
echo "cd $(pwd)" >> hklircd.sh
echo "/usr/bin/python3 hklirc.py" >> hklircd.sh
chmod +x hklircd.sh