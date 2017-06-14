#!/bin/bash

#  https://stackoverflow.com/questions/4114095/how-to-revert-git-repository-to-a-previous-commit

DIR="$1"
COMMIT="$2"

cd $DIR
git checkout master
git branch -d deadline
git checkout -b deadline $COMMIT

