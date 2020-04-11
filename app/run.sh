#!/bin/bash

umask 22
if [ "_$DEBUG" = "_" ]; then
    export PYTHONWARNINGS="ignore"
    pkill -u `id -un` "python3|gunicorn"
    sleep 10
    gunicorn --bind=127.0.0.1:${APP_PORT} \
      -w 4 \
      --timeout=1800 \
      marriage.wsgi > gunicorn.log 2>gunicorn.log </dev/null &
else
    pkill -u `id -un` "python3|gunicorn"
    sleep 10
    gunicorn --bind=127.0.0.1:${APP_PORT} \
      --log-level=DEBUG \
      --timeout=1800 \
      marriage.wsgi 
fi
