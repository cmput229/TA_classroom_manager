# Functions to handle file IO.
# -*- coding: utf-8 -*-
import json


class_csv = "./config/users.csv"
class_json = "./config/users.json"
team_csv = "./config/teams.csv"
team_json = "./config/teams.json"
inverted_teams_json = "./config/inverted_teams.json"
login_to_email = "./config/log_to_email.json"   
email_file = "./config/emails.json"
deadline_file = "./config/deadlines.csv"

def write_classlist(l):
    f = open(class_csv, "w")
    f.write(",".join(l))
    f.close()

def read_classlist():
    try:
        c_list = open(class_csv, "r")
        c = [term.strip() for term in c_list.read().split(",")]
        c_list.close()
        return c
    except:
        return []

def dump_classlist(l):
    f = open(class_json, "w")
    f.write(json.dumps(l))
    f.close()

def load_classlist():
    try:
        ci = open(class_json, "r")
        c = json.load(ci)
        ci.close()
        return c
    except:
        return {}

def read_teamslist():
    try:
        teams_list = open(team_csv, "r")
        t = [line.strip().split(",") for line in teams_list.readlines()]
        teams_list.close()
        return t
    except:
        return []

def load_teamslist():
    ti = open(team_json, "r")
    t = json.load(ti)
    ti.close()
    return t

def dump_teamslist(t):
    print "dumping"
    print t
    to = open(team_json, "w")
    json.dump(t, to)
    to.close()

def dump_inverted_teams(it):
    to = open(inverted_teams_json, "w")
    json.dump(it, to)
    to.close()

def load_inverted_teams():
    try:
        ti = open(inverted_teams_json, "r")
        t = json.load(ti)
        ti.close()
        return t
    except:
        return {}
    
def dump_login_to_email(l):
    f = open("./config/log_to_email.json", "w")
    f.write(json.dumps(l))
    f.close()

def load_login_to_email():
    try:
        f = open(login_to_email, "r")
        log2email = json.load(f)
        f.close()
        return log2email
    except:
        return {}

def load_emails():
    ei = open(email_file, "r")
    e = json.load(ei)
    ei.close()
    return e

def dump_emails(e):
    eo = open(email_file, "w")
    json.dump(e, eo)
    eo.close()

def read_deadlines():
    f = open(deadlines_file, "r")
    deadlines_file = open("./config/deadlines.csv", "r")
    d = deadlines_file.readlines()
    deadlines_file.close()

    if "\n" in d:
        d.remove("\n")
    return d

def load_defaults():
    f = open("./config/defaults.json", "r")
    defaults = json.load(f)
    f.close()
    return defaults

def read_token():
    try:
        f = open("git.token", "r")
        token = f.readline().strip()
        return token
    except:
        print("Error reading git.token.  Ensure that you have an OAuth token in git.token.")
        return None

# Param:
#   url: string representation of a GitHub resource.
# Purpose:
#   Inserts an oauth token in the url to make access easier, and to keep from committing 
#   oauth tokens to git repos.  It lets the url remain unaltered at the higher scope.
#   Needed for access using GitPython (different interface from PyGitHub).
# Returns:
#   The url, but with oauth token inserted
def auth_url(self, url):
    token = fileIO.read_token()
    url = url[:url.find("://")+3] + token + ":x-oauth-basic@" + url[url.find("github"):]
    return url

def load_assigned_repos():
    f = open("./config/assigned_repos.json", "r")
    repos = json.load(f)
    f.close
    return repos

def dump_assigned_repos(r):
    ro = open("./config/assigned_repos.json", "w")
    json.dump(r, ro)
    ro.close

# Purpose:
#   To save the repos assigned to teams to file.
def dump_repos(self, urls):
    f = open("./config/repos.json", "w")
    repos = json.dump(urls, f)
    f.close()

# Purpose:
#   To read the repos assigned to teams from file.
def load_repos(self):
    try:
        f = open("./config/repos.json", "r")
        repos = json.load(f)
        f.close()
        return repos
    except:
        return {}
