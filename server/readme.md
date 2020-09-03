## Install Steps

```
sudo apt update && sudo apt install -y virtualenv
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic
python manage.py makemigrations remote
python manage.py migrate
python manage.py createsuperuser
```
> You will need to also add your IP in `hklirc/settings.py` in the `ALLOWED_HOSTS` section if you plan to use it via wifi. For usb-network access use `10.42.0.1` which is already added.

## TODO
- Upload lircd files
- remove lirc files
- dynamic mapping view
- homepage