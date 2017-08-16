#!/bin/bash

echo "Setting virtualenv"
source venv/bin/activate
echo "--------------------------------------------------"
echo "Clearing organization."
./main.py -Q
echo ""
echo "--------------------------------------------------"
echo "Clearing defaults."
./main.py -O -R -A -S -D
echo ""
echo "--------------------------------------------------"
echo "Setting defaults."
./main.py -O GitHubClassroomTestCMPUT229 -R lab1 -A -S e337d4be.ngrok.io -D
echo ""
echo "--------------------------------------------------"
echo "Assigning teams."
./main.py -t
echo ""
echo "--------------------------------------------------"
echo "Assigning repos."
./main.py -d
echo ""
echo "--------------------------------------------------"
echo "Changing lab assignment & distributing."
./main.py -R lab3 -d
echo ""
echo "--------------------------------------------------"
echo "Changing lab and collecting repos."
./main.py -R lab1
./main.py -f
echo ""
echo "--------------------------------------------------"
echo "Clearing defaults."
./main.py -Q
./main.py -O -R -A -S -D
echo ""
echo "--------------------------------------------------"
echo ""
