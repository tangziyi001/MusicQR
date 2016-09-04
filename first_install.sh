#!/bin/bash
set +x
virtualenv env
source ./env//bin/activate
pip install -r requirements.txt
