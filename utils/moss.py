#!/usr/bin/env python

import os
import shutil
import subprocess

# Params:
#   lab: string identifier for lab
# Purpose:
#   Expects base code to be in ./submissions/<lab>/base/submission/
#   Gathers a list of all base code files for a given lab.
#   Appends a flag for moss to the front of the file name
# Returns:
#   A list of flags to be passed into Moss to identify base code files.
def getBase(lab):
    base_dir = "./submissions/{}/base/".format(lab)
    base_files = os.listdir("./submissions/{}/base/".format(lab))
    base_files.sort()
    for f in base_files:
        if f.find(".s") == -1:
            base_files.remove(f)
    base_flags = ["-b {}{}".format(base_dir, f) for f in base_files]
    return base_flags

# Params:
#   archives: string identifier for archive folder
# Purpose:
#   Expects archives to be within ./submissions/<archives>/
#   Gathers a list of all files within the archives folder
#   Generates a list of these files to pass in to MOSS
# Returns:
#   A list of files to be passed to MOSS
def getArchives(archives):
    if archives == "":
        return ""
    a = os.listdir("./submissions/{}/".format(archives))
    for filename in a:
        newname = "".join(filename.split(" "))
        if newname != filename:
            os.rename("./submissions/{}/{}".format(archives, filename), 
                      "./submissions/{}/{}".format(archives, newname))
    a = os.listdir("./submissions/{}/".format(archives))
    a = ["./submissions/{}/\"{}\"".format(archives, filename) for filename in a]
    return a    

# Params:
#   lab: string identifier for the lab
# Purpose:
#   Expects submissions to be in ./submissions/<lab>/<team>/submission/
#   To gather all the student submissions to pass in to MOSS.
def getSubmissions(lab):
    submissions = os.listdir("./submissions/{}/".format(lab))
    submissions.remove("base")
    submissions = ["./submissions/{}/{}/".format(lab, team) for team in submissions]
    files = []
    for submission in submissions:
        fs = os.listdir(submission)
        for f in fs:
            if f.find(".s") != -1:
                files.append("{}{}".format(submission, f))
    return files

# Expects repos to be gathered when called.
# Base code to be in ./<lab>/instructor/base/
# Student submissions to be in ./<lab>/<team>/submission/
# Archived submissions to be in ./<lab>/archived/

# Troubleshooting File name too long error
# https://stackoverflow.com/questions/6441507/executing-python-scripts-with-subprocess-call-using-shebang
# User: Chris
def submit(lab, lang="mips", suffix="s", archives=""):
    print "Submitting repos to moss."
    print "This may take quite a long time."

    lab_dir = "./submissions/{}/".format(lab)    
    base_flags = getBase(lab)
    archives = getArchives(archives)
    submissions = getSubmissions(lab)

    # W/pairwise comparison
    # command = "./moss/mossScript {} ./moss/moss -l {} ".format(lab, lang)    
    # Wout/pairwise comparison
    command = "./moss/mossScript {} ./moss/moss -l {} -d ".format(lab, lang)
    for base_file in base_flags:
        command += base_file + " "
    for archived_file in archives:
        command += archived_file + " "
    for submission in submissions:
        command += submission + " "
    command = command.strip()

    if os.path.isdir("./moss/results/{}".format(lab)):
        shutil.rmtree("./moss/results/{}".format(lab))
        os.mkdir("./moss/results/{}".format(lab))

    subprocess.call(command, shell=True)


    


