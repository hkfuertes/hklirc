#!/bin/bash

# Check for SU
if [[ $(id -u) -ne 0 ]] ; then echo "Please run as root" ; exit 1 ; fi

DEFAULT_PATH="/home/pi/hklirc/server"

# Installing virtualenv
tput setaf 2; echo "[+] Installing virtualenv";tput setaf 7;
apt install -y virtualenv

# Creating and activating virtualenv
tput setaf 2; echo "[+] Creating and activating virtualenv";tput setaf 7;
virtualenv -p python3 venv
source venv/bin/activate

# Configuring django project
tput setaf 2; echo "[+] Creating and activating virtualenv";tput setaf 7;
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py makemigrations remote
python manage.py migrate
#python manage.py createsuperuser

# Make sure that the lircd.conf.d folder exists and everyone can read and write to it.
tput setaf 2; echo "[+] Making sure that the remotes folder exists and that its readable";tput setaf 7;
mkdir -p /etc/lirc/lircd.conf.d/
chmod 777 /etc/lirc/lircd.conf.d/

# Creating an example mapping
tput setaf 2; echo "[+] Creating an example mapping";tput setaf 7;
python manage.py example_mapping

# Installing Service
tput setaf 2; echo "[+] Installing Service";tput setaf 7;
sed -i "s|^\(DJANGODIR\s*=\s*\).*\$|\1$(pwd)|g" hklirc-config-start.sh
sed -i "s|$DEFAULT_PATH|$(pwd)|g" hklirc-config.service
cp hklirc-config.service /etc/systemd/system/
systemctl enable hklirc-config.service