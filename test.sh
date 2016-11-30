#!/bin/bash
source ./env/bin/activate
echo 'Run server'
python ./lswa/manage.py runserver
