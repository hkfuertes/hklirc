## dJango Server for hklirc
Simple server solution to manage the mappings. To access it go to `http://10.42.0.1:8000` when using the usb-ethernet gadget, and `http://<raspberrypi-ip>:8000` when accessing via Wifi.

> You will need to also add your IP in `hklirc/settings.py` in the `ALLOWED_HOSTS` section if you plan to use it via wifi.

## Installation
`# install_server.sh`

## TODO
- Homepage
- Deploy with gunicorn + nginx!
