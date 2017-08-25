# Functions to handle file IO.
import json


class_csv = "./config/users.csv"
class_json = "./config/users.json"
team_csv = "./config/teams.csv"
team_json = "./config/teams.json"
login_to_email = "./config/log_to_email.json"   
email_file = "./config/emails.json"
deadline_file = "./config/deadlines.csv"

def write_classlist(l):
    f = open(class_csv, "w")
    f.write(",".join(l))
    f.close()

def read_classlist():
    c_list = open(class_csv, "r")
    c = [term.strip() for term in c_list.read().split(",")]
    c_list.close()
    return c

def dump_classlist(l):
    f = open(class_json, "w")
    f.write(json.dumps(l))
    f.close()

def load_classlist():
    ci = open(class_json, "r")
    c = json.load(ci)
    ci.close()
    return c

def read_teamslist():
    teams_list = open(team_csv, "r")
    t = [line.strip().split(",") for line in teams_list.readlines()]
    teams_list.close()
    return t

def dump_teamslist(t):
    to = open(team_json, "w")
    json.dump(t, to)
    to.close()

def load_teamslist():
    ti = open(team_json, "r")
    t = json.load(ti)
    ti.close()
    return t
    
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


