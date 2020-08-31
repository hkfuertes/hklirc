## helpful links
- https://github.com/d-demirci/django-adminlte3
- https://django-bootstrap4.readthedocs.io/en/latest/quickstart.html#example-template
- https://stackoverflow.com/questions/473620/how-do-you-create-a-daemon-in-python
- https://stackoverflow.com/questions/4637420/efficient-python-daemon

## Missing steps
- Install virtualenv and python3-dev to be able to compile and install python3-cwiid
- Enable the gpio-ir pins in config.txt (in my case pin 14)
- python manage.py makemigrations remote & migrate
- python manage.py createsuperuser
- for now create a mapping from admin app (django)
- add your servers' ip to allowedhosts in django