#!/bin/bash

NAME="hklirc"                              #Name of the application (*)
DJANGODIR=/home/pi/hklirc/server             # Django project directory (*)
#SOCKFILE=/home/pi/hklirc/gunicorn.sock        # we will communicate using this unix socket (*)
USER=pi                                        # the user to run as (*)
GROUP=pi                                     # the group to run as (*)
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=hklirc.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=hklirc.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
#RUNDIR=$(dirname $SOCKFILE)
#test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=0.0.0.0:8000
