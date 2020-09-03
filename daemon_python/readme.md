## Install Steps
- `sudo apt update && sudo apt install -y lirc`
- Change `driver=default` and `device=/dev/lirc0` in `/etc/lirc/lirc_options.conf` 
  > _Need to come up with a `sed` command to do this!_
- Uncomment and change `dtoverlay=gpio-ir,gpio_pin=17` from `/boot/config.txt`, in my case using pin **14**.
  > _Need to come up with a `sed` command to do this!_
- Add any remote to `/etc/lirc/lircd.conf.d/` and reboot to make lircd pick them.
- `$ python3 hklirc.py`
- **Don't** run python script as root!