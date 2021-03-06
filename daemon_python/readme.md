## Installation
`# ./install_daemon.sh`

This script will execute the steps bellow automatically. **It has to be run by root.**

## Manual Steps
- `sudo apt update && sudo apt install -y lirc`
- Change `driver=default` and `device=/dev/lirc0` in `/etc/lirc/lirc_options.conf` 
  > _Need to come up with a `sed` command to do this!_
- Uncomment and change `dtoverlay=gpio-ir,gpio_pin=17` from `/boot/config.txt`, in my case using pin **14**.
  > _Need to come up with a `sed` command to do this!_
- Add any remote to `/etc/lirc/lircd.conf.d/` and reboot to make lircd pick them.
- Modify launcher (`hklird.sh`) with the correct folder, and install the service (`hklircd.service`).
- `$ python3 hklirc.py` _(**Don't** run python script as root!)_

## Defaults
- Remote: https://sourceforge.net/p/lirc-remotes/code/ci/master/tree/remotes/sony/SCPH-10150.lircd.conf
- GPIO PIN: **14**
