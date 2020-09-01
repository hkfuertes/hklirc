## Install Steps

```
sudo apt update && sudo apt install -y virtualenv
virtualenv -p python3 venv
source venv/bin/activate
python manage.py makemigrations remote
python manage.py migrate
python manage.py createsuperuser
```

- You will need to also add your ip in `hklirc/settings.py` in the `ALLOWED_HOSTS` section. 
- And you also need to create (_**for now**_) a first mapping via django admin page.