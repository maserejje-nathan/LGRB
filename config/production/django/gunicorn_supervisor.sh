#!/bin/bash
NAME="lgrb_els"                                  # Name of the application
DJANGODIR=/home/user1/LGRB_ELS/lgrb_els        # Django project directory
USER=root
GROUP=root
NUM_WORKERS=2                                      # how many worker processes should Gunicorn spawn
TIMEOUT=300
DJANGO_SETTINGS_MODULE=lgrb_els.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=lgrb_els.wsgi                     # WSGI module name
PORT=9755
LOCAL_IP="127.0.0.1"
echo "Starting $NAME as `whoami`"
cd $DJANGODIR
source /home/user1/LGRB_ELS/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
exec /home/user1/LGRB_ELS/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --timeout $TIMEOUT \
  --user=$USER --group=$GROUP \
  --pythonpath=/home/user1/LGRB_ELS/venv/bin \
  --log-level=debug \
  --bind=$LOCAL_IP:$PORT \
  --log-file=-