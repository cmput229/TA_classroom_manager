#!/usr/bin/env python

import sys
import json

from utils.classroom_manager import *
import spimgrader as grader
import utils.moss

# flags:  
def help():  
    return """--------------------------------------------------------------------
    This is a list of flags on the command-line:

    -o <organization_name>: set organization name           ([o]rg set)
    -r <repo_name>: set repo for script                     ([r]epo set)
    -t: set teams for the organization locally              ([t]eams set)
    -a <team_name> <member>: Add <member> to <team>         ([a]dd member)
    -d <team_name> <member>: delete <member> from <team>    ([d]emove member)
    -s: distribute base repo (-r <repo>) to teams on GitHub ([s]et repos)
    -n: notify students of repo distribution                ([n]otify)
    -g: collect repos (-r <base_repo>) from students        ([g]et repos)
    -A: <archive_folder>: set archive directory             ([a]rchive set)
    -m: mark repos
    -c: compare repos using MOSS
    -x: clear local repos (-r <assignment>)
    -X: clear teams & repos on GitHub
    --------------------------------------------------------------------
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

    if "-h" in args:
        print help()
        return

    # SETUP
    #----------------------------------------------------------------------------------
    if "-o" in args:
        defs["org"] = parse_flag("-o", args)[0]

    if "-r" in args:
        defs["repo"] = parse_flag("-r", args)[0]

    if "-A" in args:
        defs["archives"] = parse_flag("-A", args)[0]
    
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
    
    if "-n" in args:
        m.notify_all(defs["repo"])              # Notification for repo distribution
        return

    if "-g" in args:
        m.get_repos(defs["repo"])               # get github repos

    if "-m" in args:
        grader.main(defs["repo"])

    if "-c" in args:
        moss.submit(defs["repo"], defs["archives"])

    if "-x" in args:
        print "THIS WILL CLEAR THE LOCAL REPOS FOR {}.".format(repo_name)
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
