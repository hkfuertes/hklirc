## Install Steps
- `sudo apt update && sudo apt install -y lirc`
- Change `driver=default` and `device=/dev/lirc0` in `/etc/lirc/lirc_options.conf` 
  > _Need to come up with a `sed` command to do this!_
- Uncomment and change `dtoverlay=gpio-ir,gpio_pin=17` from `/boot/config.txt`
  > _Need to come up with a `sed` command to do this!_
- Add any remote to `/etc/lirc/lircd.conf.d/` and reboot to make lircd pick them.
- Generate a `all_codes.conf` config file with `configGenerator/genconf.py`
- Run `irexec all_codes.conf` with the `-d` option to have it in background.
  > _Need to come with a linux service for this!_
