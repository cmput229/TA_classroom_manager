#!/bin/bash

echo $1
cd ./tmp/dummy-repo
ls
git remote add origin $1
git push -u origin master
