#!/bin/bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cd ./gmail
pip install --upgrade google-api-python-client
cd ../
python ./gmail/quickstart.py
deactivate
