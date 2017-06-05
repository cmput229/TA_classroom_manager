#!/usr/bin/env python

import sys
import os.path
import shutil
import json
import subprocess

# Expects base code to be in ./<lab>/instructor/base/
# Want to handle more than just *.s; just concat. all *.* in /base/
def makeBase(lab, suffix = "s"):
    base_dir = "./marker/base/{}/".format(lab)
    base_file = "./marker/base/{}.{}".format(lab, suffix)

    files = os.listdir(base_dir)
    files.sort()

    base = open(base_file, "w")     # Make new base file
    for f in files:
        f = open("{}{}".format(base_dir, f), "r")
        base.write(f.read())
        f.close()
    base.close()

    return base_file                # Return path to base file

# Expects repos to be gathered when called.
# Base code to be in ./marker/<lab>/instructor/base/
# Student submissions to be in ./marker/<lab>/<team>/submission/
# Archived submissions to be in ./marker/<lab>/archived/
def submit(lab, lang="mips", suffix="s"):
    print "Submitting repos to moss."

    lab_dir = "./marker/{}/*.{}".format(lab, suffix)
    if os.path.isdir("./marker/{}/archived/".format(lab)):
        archives = "./marker/{}/archived/*.{}".format(lab, suffix)
    else:
        archives = ""

    if os.path.isdir("./moss/results/{}".format(lab)):
        shutil.rmtree("./moss/results/".format(lab))
    
    base_file = makeBase(lab, suffix)
    
    command = "./moss/mossScript {} {} {}".format(lang, lab, archives)
    command = command.strip()
    command = command.split(" ")
    subprocess.call(command)

#------------------------------------------------------------------------------
# Clears all ./<lab>/ repos from cwd.
# Handy to tidy up after running the test and peeking at what gets pulled.
#------------------------------------------------------------------------------
def clear(lab):
        shutil.rmtree("./{}/".format(lab))

# flags:    -l <lab_name>: set lab name
#           -r <repo_name>: set repo for script
#           -b: concatenate all base files into one file        (Set [b]ase code)
#           -s: submit code to moss                             ([S]ubmit)
#           -g: collect repos (-r <base_repo>) from students    ([G]et repos)
#           -x: clear local responses from moss
#           -X: clear all local files
def main():
    lab = "testlab1"
    args = sys.argv

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

    if "-s" in args:
        submit(lab)

if __name__ == "__main__":
    main()

    


