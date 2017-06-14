#!/bin/bash

# https://stackoverflow.com/questions/4114095/how-to-revert-git-repository-to-a-previous-commit
# https://www.git-tower.com/learn/git/faq/restore-repo-to-previous-revision
# https://stackoverflow.com/questions/8943693/can-git-operate-in-silent-mode
# http://www.tldp.org/LDP/abs/html/io-redirection.html

DIR="$1"
COMMIT="$2"

cd $DIR
git checkout master -q                     # Ensure we're on the master
git branch -d deadline -q                  # Ensure that there isn't already a deadline branch
git checkout -b deadline $COMMIT -q        # Create & checkout a new branch called deadline at or before the deadline
git push --set-upstream origin deadline -q # Creates a remote upstream branch; lets students see what's being marked.

