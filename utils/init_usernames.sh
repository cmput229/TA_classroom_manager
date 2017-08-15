#!/bin/bash

mkdir tmp
cd ./tmp
git clone https://github.com/Klortho/get-github-usernames.git . # Clone repo that allows us to get usernames
npm install
cp ../config/users.txt ./users.txt
node ./index.js


