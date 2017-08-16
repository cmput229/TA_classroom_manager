#!/bin/bash

echo "Setting virtualenv"
source venv/bin/activate

clear
echo "Clearing organization."
./main.py -Q
read -p "Press a key to begin the demo."
clear

echo "Clearing defaults."
./main.py -O -R -A -S -D
read -p "Press a key to set defaults."
clear

echo "Setting defaults."
./main.py -O GitHubClassroomTestCMPUT229 -R lab1 -A -S e337d4be.ngrok.io -D
read -p "Press a key to assign teams."
clear

echo "Assigning teams."
./main.py -t
read -p "Press a key to assign repos."
clear

echo "Assigning repos."
./main.py -d
read -p "Press a key to change lab."
clear

echo "Changing lab assignment & distributing."
./main.py -R lab3 -d
read -p "Press a key to change to lab1 and collect."
clear

echo "Collecting repos."
./main.py -R lab1
./main.py -f
read -p "Press a key to finish the demo."
clear

./main.py -Q
./main.py -O -R -A -S -D
