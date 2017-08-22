#!/bin/bash

if ! [ -a ./git.token ]
    then
        echo "You need to obtain an OAuth token from Github to set this service up."
        echo "Obtain one by following instructions at:"
        echo "https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/"
        exit
fi

if ! [ -a ./client_secret.json ]
    then
        echo "You need to obtain an OAuth token for Google's Gmail API to set this service up."
        echo "Obtain one by following instructions at:"
        echo "https://developers.google.com/gmail/api/quickstart/python"
        exit
fi

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
cd ./gmail
pip install --upgrade google-api-python-client
cd ../
python ./gmail/quickstart.py
deactivate
