#!/bin/bash

if [ "dev" == "$1" ]; then
    echo "RUN 'dev'"
    FLASK_APP=dev_main.py FLASK_ENV=development flask run -p 3000
elif [ "prod" == "$1" ]; then
    echo "RUN 'prod'"
    FLASK_APP=main.py FLASK_ENV=development flask run -p 3000
else
    echo "you can choose in ['dev', 'prod']"
fi
