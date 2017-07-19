#!/usr/bin/env python

import sys
import json

from utils.classroom_manager import *
from utils import spimgrader as grader
import utils.moss

# flags:  
def help():  
    return """---------------------------------------------------------------------------------------
|   This is a list of flags for the command-line:
|
|   INFO
|=====================================================================================
|   -h: print help                                          ([h]elp)
|   -D: print defaults                                      ([D]efaults)
|
|   SETUP
|=====================================================================================
|   -p <prefix>: set optional prefix for assignments        (set [p]refix)
|   -S <server url>: set server url                         (set [S]erver)
|   -o <organization_name>: set organization name           ([o]rg set)
|   -r <repo_name>: set repo for script                     ([r]epo set)
|   -A <archive_folder>: set archive directory              ([a]rchive set)
|   -j: create Jobs DSL file for Jenkins                    ([j]obs DSL)
|   -t: set teams for the organization locally              ([t]eams set)
|   -a <team> <member>: Add <member> to <team>              ([a]dd member)
|   -d <team> <member>: delete <member> from <team>         ([d]emove member)
|
|   DISTRIBUTION
|=====================================================================================
|   -s (-r <repo>): distribute base repo to teams on GitHub ([s]et repos)
|   -g (-r <base_repo>): collect repos from students        ([g]et repos)
|   -w (-r <repo>): set webhooks for teams working on repo  (set [w]ebhooks)
|   -n: notify students of repo distribution                ([n]otify)
|
|   HOUSEKEEPING
|=====================================================================================
|   -m: mark repos                                          ([m]ark repos)
|   -c: compare repos using MOSS                            ([c]ompare)
|   -x: clear local repos (-r <assignment>)                 ()
|   -X: clear teams & repos on GitHub                       ()
|
---------------------------------------------------------------------------------------
    """

# Purpose:
#   Returns a dictionary used to represent default values for the manager to use.
def defaults():
    try:
        f = open("./config/defaults.json", "r")
        defaults = json.load(f)
        f.close()   
        return defaults
    except:
        return {"org": "", "repo": "", "archives": ""}

# Param:
#   field: field in defaults.json to be update.
#   new_value: the value to overwrite where the field is.
# Purpose:
#   Updates the default values used for the manager to the most-recently used ones.
def update(defs):
    try:
        f = open("./config/defaults.json", "w")
        json.dump(defs, f)
        f.close()
        return
    except:
        return

def pretty(defs):
    p = "---------------------------------------------------------------------------------------\n"
    p += "| Current Values Used by the Classroom Manager\n"
    p += "|\n"
    for k, v in defs.items():
        if k == "repo" or k == "org":
            p += "| {}:\t\t{}\n".format(k, v)
        else:
            p += "| {}:\t{}\n".format(k, v)
    p += "---------------------------------------------------------------------------------------"
    return p

def parse_flag(flag, args):
    start = args.index(flag)+1
    end = start
    while end < len(args):
        if args[end][0] == "-":
            break
        end += 1
    if start == end:
        return [""]
    else:
        return args[start:end]

def main():
    defs = defaults()
    args = sys.argv

    if "-h" in args or "-H" in args or "--help" in args:
        print help()
        return

    if "-D" in args:
        print pretty(defs)

    # SETUP
    #----------------------------------------------------------------------------------
    if "-p" in args:
        print "Updating prefix."
        defs["prefix"] = parse_flag("-p", args)[0]

    if "-o" in args:
        print "Updating organization."
        defs["org"] = parse_flag("-o", args)[0]

    if "-r" in args:
        print "Updating repo."
        defs["repo"] = parse_flag("-r", args)[0]

    if "-A" in args:
        print "Updating archives."
        defs["archives"] = parse_flag("-A", args)[0]

    if "-S" in args:
        print "Updating server."
        defs["server"] = parse_flag("-S", args)[0]
    
    update(defs)

    # WORK
    #----------------------------------------------------------------------------------
    m = Manager(defs["org"])

    if "-t" in args:
        m.set_teams()                           # local
        m.set_git_teams()                       # remote
        m.git_to_csv()                          # setup csv for teams

    if "-a" in args:
        flag_args = parse_flag("-a", args)      # parse
        team = flag_args[0]                     # set team
        members = flag_args[1:]                 # set members
        m.add_members(team, members)            # add

    if "-d" in args:
        flag_args = parse_flag("-d", args)      # parse
        team = flag_args[0]                     # set team
        members = flag_args[1:]                 # set members
        m.del_members(team, members)            # delete
    
    if "-s" in args:
        m.set_repos(defs["repo"])               # Set github repos

    if "-w" in args:
<<<<<<< HEAD
        m.set_hooks(defs["repo"])               # Set webhooks to distributed repos
    
    if "-j" in args:
        m.write_jobs_repos("Lab_Template")      # Set the repos component of .groovy DSL
        m.make_jobs_DSL("Lab_Template")         # Concatenate components of DSL into valid file
=======
        m.set_hooks(defs["repo"])            # Set webhooks to distributed repos
>>>>>>> c03a959b476282926d9bca6b6834170dab6092a1
    
    if "-n" in args:
        m.notify_all(defs["repo"])              # Notification for repo distribution

    if "-g" in args:
        m.get_repos(defs["repo"])               # Get github repos

    if "-m" in args:
        grader.main(defs["repo"])               # Grade with spimgrader

    if "-c" in args:
        moss.submit(defs["repo"], archives=defs["archives"])    # Submit to Moss

    if "-x" in args:
        print "THIS WILL CLEAR THE LOCAL REPOS FOR {}.".format(defs["repo"])
        confirm = (raw_input("Are you sure? [y/n]: ")[0].lower() == 'y')
        if confirm:
            m.del_local_repos(defs["repo"])     # remove local repos

    if "-X" in args:
        print "THIS WILL CLEAR ALL TEAM REPOS & TEAMS FROM GitHub."
        confirm = (raw_input("Are you sure? [y/n]: ")[0].lower() == 'y')
        if confirm:
            m.del_git_repos()                   # remove remote repos
            m.del_git_teams()                   # remove remote teams
    return

if __name__ == "__main__":
    main()
