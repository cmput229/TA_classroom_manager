#!/bin/bash

if ! [ -e git.token ]
    then
        echo "Please provide a git.token."
        exit
fi

echo "Setting virtualenv"
source venv/bin/activate
echo "--------------------------------------------------"
echo "Clearing organization."
echo "--------------------------------------------------"
echo ""
./main.py -Q
echo ""
echo "--------------------------------------------------"
echo "Clearing defaults."
echo "--------------------------------------------------"
echo ""
./main.py -O -R -A -S -D
echo ""
echo "--------------------------------------------------"
echo "Setting defaults."
echo "--------------------------------------------------"
echo ""
./main.py -O GitHubClassroomTestCMPUT229 -R lab1 -A -S e337d4be.ngrok.io -D
echo ""
echo "--------------------------------------------------"
echo "Assigning teams."
echo "--------------------------------------------------"
echo ""
./main.py -t
echo ""
echo "--------------------------------------------------"
echo "Assigning repos."
echo "--------------------------------------------------"
echo ""
./main.py -d
echo ""
echo "--------------------------------------------------"
echo "Changing lab assignment & distributing."
echo "--------------------------------------------------"
echo ""
./main.py -R lab3 -d
echo ""
echo "--------------------------------------------------"
echo "Changing lab and collecting repos."
echo "--------------------------------------------------"
echo ""
./testing/lab1/demo.sh
read -p "Pausing" -t 5
echo ""
./main.py -R lab1
./main.py -f
echo ""
echo "--------------------------------------------------"
echo "Clearing defaults."
echo "--------------------------------------------------"
echo ""
./main.py -Q
./main.py -O -R -A -S -D
echo ""
echo "--------------------------------------------------"
echo ""
echo ""
deactivate
