#!/bin/bash
echo 'Go to http://35.163.220.222:8000/micro/'
source ./env/bin/activate && python ./web/scalica/manage.py runserver 0.0.0.0:8000
