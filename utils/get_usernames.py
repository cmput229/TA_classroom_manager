# Uses init_usernames.sh to establish a repo cloning https://github.com/Klortho/get-github-usernames.git
# * Installs npm to permit the repo's use.
# * Copies config/users.txt into that folder to inform the tool what github emails are boeing used.
# * Calls node ./index.js to create dummy commits for each user identified by email.
#   * Github maps the command-line git commits made to the dummy-repo to the users associated with those emails.
# Uses pygithub to create a new repo on Github.
# Use gitpython to push the dummy repo to Github.
# Uses pygithub to comb through the commits made to that repo.
# Pull the usernames in.
# Write the usernames to file in config/users.csv
# Delete the github repo after getting usernames.
# Delete the local repo.
# Delete the cloned repo.

from github import Github
from git import Repo
import subprocess
import shutil

def main():
    usernames = []
    subprocess.call(["node ./usernames/index.js"])
    a = raw_input()


main()
