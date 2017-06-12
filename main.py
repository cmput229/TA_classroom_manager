#!/usr/bin/env python

import sys
import json


from utils.classroom_manager import *
import spimgrader as grader
import moss

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
        return None

# Param:
#   field: field in defaults.json to be update.
#   new_value: the value to overwrite where the field is.
# Purpose:
#   Updates the default values used for the manager to the most-recently used ones.
def update(field, new_value):
    try:
        f = open("./config/defaults.json", "r")
        defaults = json.load(f)
        f.close()
        defaults[field] = new_value
        f = open("./config/defaults.json", "w")
        json.dump(defaults, f)
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
    return args[start:end]

def main():
    org_name = ""
    repo_name = ""
    arch_name = ""
    args = sys.argv

    if "-h" in args:
        print help()
        return

    if "-o" in args:
        org_name = parse_flag("-o", args)
    elif defaults():
        try:
            org_name = defaults()["org"]
        except:
            print "Error with org name"
            return 1

    if "-r" in args:
        repo_name = parse_flag("r", args)    # Set lab name
        update("repo", repo_name)
    elif defaults():
        try:
            repo_name = defaults()["repo"]
        except:
            print "Error with repo name."
            return 1

    if "-A" in args:
        arch_name = parse_flag("-A", args)[0]
        update("archives", arch_name)
    elif defaults():
        try:
            arch_name = defaults()["archives"]
        except:
            print "Error with archive name."
            return 1

    m = Manager(org_name)

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
        m.set_repos(repo_name)                  # Set github repos
    
    if "-n" in args:
        m.notify_all(repo_name)                 # Notification for repo distribution
        return

    if "-g" in args:
        m.get_repos(repo_name)                  # get github repos

    if "-m" in args:
        grader.main(repo_name)

    if "-c" in args:
        moss.submit(repo_name, archives=arch_name)

    if "-x" in args:
        print "THIS WILL CLEAR THE LOCAL REPOS FOR {}.".format(repo_name)
        confirm = (raw_input("Are you sure? [y/n]: ")[0].lower() == 'y')
        if confirm:
            m.del_local_repos(repo_name)        # remove local repos

    if "-X" in args:
        print "THIS WILL CLEAR ALL TEAM REPOS & TEAMS FROM GitHub."
        confirm = (raw_input("Are you sure? [y/n]: ")[0].lower() == 'y')
        if confirm:
            m.del_git_repos()                   # remove remote repos
            m.del_git_teams()                   # remove remote teams
    return

if __name__ == "__main__":
    main()
