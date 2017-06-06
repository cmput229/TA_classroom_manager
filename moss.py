#!/usr/bin/env python

import sys
import os
import shutil
import json
import subprocess

# Expects base code to be in ./<lab>/instructor/base/
# Want to handle more than just *.s; just concat. all *.* in /base/
def makeBase(lab, suffix = "s"):
    base_dir = "./submissions/{}/base/submission/".format(lab)
    base_files = os.listdir("./submissions/{}/base/submission/".format(lab))
    base_files.sort()
    base_flags = ["-b {}{}".format(base_dir, f) for f in base_files]
    return base_flags

# Expects repos to be gathered when called.
# Base code to be in ./<lab>/instructor/base/
# Student submissions to be in ./<lab>/<team>/submission/
# Archived submissions to be in ./<lab>/archived/
def submit(lab, lang="mips", suffix="s"):
    print "Submitting repos to moss."

    lab_dir = "./submissions/{}/".format(lab)    
    base_flags = makeBase(lab, suffix)
    submissions = os.listdir(lab_dir)
    submissions.remove("base")
    
    command = "./moss/moss -l {} -d ".format(lang)
    for base_file in base_flags:
        command += base_file + " "
    
    for submission in submissions:
        files = os.listdir("{}{}/submission/".format(lab_dir, submission))
        for f in files:
            command += "{}{}/submission/{}".format(lab_dir, submission,f) + " "
    command = command.strip()
    # command = command.split(" ")
    subprocess.call(["./moss/mossScript", command])

    # subprocess.call(command)

#------------------------------------------------------------------------------
# Clears all ./<lab>/ repos from cwd.
# Handy to tidy up after running the test and peeking at what gets pulled.
#------------------------------------------------------------------------------
def clear(lab):
        shutil.rmtree("./{}/".format(lab))

# flags:    -l <lab_name>: set lab name
#           -r <repo_name>: set repo for script
#           -s: submit code to moss                             ([S]ubmit)
#           -g: collect repos (-r <base_repo>) from students    ([G]et repos)
#           -x: clear local responses from moss
#           -X: clear all local files
def main():
    lab = "testlab1"
    args = sys.argv
    archives = False 

    if "-x" in args:
        print "CLEARING RESULTS"
        clear("results")
        return

    if "-X" in args:
        print "THIS WILL CLEAR ALL LOCAL INFO FOR {}.".format(lab)
        confirm = (raw_input("Are you sure? [y/n]: ")[0].lower() == 'y')
        if confirm:
            clear(results)
            clear(lab)
            return 

    if "-l" in args:
        lab = args[args.index("-l")+1]

    if "-a" in args:
        archives = True

    if "-s" in args:
        submit(lab)

if __name__ == "__main__":
    main()

    


