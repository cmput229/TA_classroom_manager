#!/bin/bash

#  https://stackoverflow.com/questions/4114095/how-to-revert-git-repository-to-a-previous-commit

URL="$1"
DIR="$2"
COMMIT="$3"

cd $DIR
git checkout -b deadline $COMMIT
git stash
git fetch origin deadline

