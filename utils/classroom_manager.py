#!/usr/bin/env python

import json
import shutil
from github import Github
from git import Repo
import git
from datetime import datetime
from datetime import timedelta
from time import sleep
import os
import subprocess

import spimgrader as grader
import moss
from notifier import send_notification as notify
import fileIO


# REFERENCE
#----------------------------------------------------------------------------------------------
# Oauth tokens in gitpython    
# http://stackoverflow.com/questions/36358808/cloning-a-private-repo-using-https-with-gitpython
# User: shawnzhu
#
# Organizations & Membership
# https://github.com/PyGithub/PyGithub/issues/507
# User: lbrownell-gpsw
#
# Pushing to remote with gitpython
# https://stackoverflow.com/questions/41429525/how-to-push-to-remote-repo-with-gitpython
# User: zmo
#----------------------------------------------------------------------------------------------

# STRUCTURE OF THE MANAGER
#----------------------------
#   - init()
#   - set_members()
#
#   TEAM METHODS
#   -------------------------
#   - set_teams
#   - set_git_teams
#   - get_git_teams
#   - del_git_teams
#   - add_members
#   - del_members
#   - get_usernames
#
#   DISTRIBUTION METHODS
#   -------------------------
#   - is_assigned
#   - set_base
#   - remote_clone
#   - local_clone
#   - assign_repos
#   - set_repos
#   - get_repos
#   - del_local_repos
#   - del_git_repos
#
#   WEBHOOK METHODS
#   -------------------------
#   - clean_hooks
#   - make_hook
#   - set_hooks
#
#   JENKINS METHODS
#   -------------------------
#   - make_jobs_DSL
#
#   NOTIFICATION METHODS
#   -------------------------
#   - notify_all
#
#   COLLECTION METHODS
#   -------------------------
#   - get_commits
#   - get_deadline
#   - get_repo_by_deadline
#
#   HOUSEKEEPING METHODS
#   -------------------------
#   - gen_repo_name
#   - get_server
#   - json_to_csv
#   - git_to_csv
#   - remove_local
#   - insert_auth
#   - load_repos
#   - write_repos

class Manager():
    def __init__(self, name):
        self.name = name
        self.url = "https://github.com/{}/".format(name)
        token = fileIO.read_token()
        self.hub = Github(token)        
        self.org = self.hub.get_organization(name)

    # Params:
    #   hub: PyGitHub github object
    #   org: PyGitHub organization object
    # Purpose:
    #   To iterate over all the GitHub IDs in a class.txt file
    #   and add the GitHub users to the organization's membership.
    # N.B.: class.txt is a text file with student gitIDs on each line
    # TODO: REMOVE THIS?  NOT USED.  ASSUME STUDENTS MUST JOIN ORGANIZATION?
    def set_members(self):
        c = fileIO.read_classlist()

        for student in c:
            self.org.add_to_public_members(self.hub.get_user(student))

    # TEAM METHODS
    #----------------------------------------------------------------------------------

    # Default:      Each student in the class is in their own team
    # Nondefault:   If students are allowed to form groups, then their groups should
    #               be identified in teams.txt
    # Should check that students are not member of more than one group.
    # class.txt is a text file with student gitIDs on each line
    # teams.txt is a text file that identifies which student gitIDs are proposed
    # to be group members.  Groups should be in csv format.
    def initialize_git_teams(self):
        print "Parsing class & team files."
        teams = {}

        c = fileIO.read_classlist()
        t = fileIO.read_teamslist()
        max_team = get_max_team(self.org)

        for team in t:
            teams[max_team] = team
            max_team = "team{}".format(int(max_team[4:]) + 1)
            for member in team:
                if member in c:
                    c.remove(member)

        for line in c:
            line = line.strip()
            teams[max_team] = [line]
            max_team = "team{}".format(int(max_team[4:]) + 1)
        
        fileIO.dump_teamslist(teams)
        
        inverted_teamslist = {}
        for team in teams.keys():
            for member in teams[team]:
                inverted_teamslist[member] = team
        
        fileIO.dump_inverted_teams(inverted_teamslist)

    # Params:
    #   hub: PyGitHub github object
    #   org: PyGitHub organization object
    # Purpose:
    #   To iterate over all the teams defined locally with team_defs.json
    #   and create teams on GitHub.
    def set_git_teams(self):
        print "Setting teams on GitHub."

        local_teams = fileIO.load_teamslist()
        remote_teams = get_remote_team_names(self.org)
        
        for team_name in local_teams.keys():
            if team_name not in remote_teams:
                t = self.org.create_team(team_name)
                for member in local_teams[team_name]:
                    t.add_to_members(self.hub.get_user(member))
            else:
                print "{} already exists.".format(team_name)

    # Takes an updated version of the class list as if from LDAP
    # Looks-up usernames of students that have dropped, and removes them from the class.
    # Looks-up usernames of students that have joined the class, and adds them to the teams appropriate.
    # Distributes any repos that have been already distributed to the new students.
    # ASSUMPTION:
    # users.txt is the current snapshot of the class
    def update_git_teams(self):
        updated_class = set(fileIO.read_classlist())
        teams = fileIO.load_teamslist()
        inverted_teams = fileIO.load_inverted_teams()

        # Remove members who have dropped
        for member in inverted_teams.keys():
            if member not in updated_class:
                team = inverted_teams[member]
                self.del_members(team, [member])    # Update remote
                del(inverted_teams[member])         # Update inverted index
                teams[team].remove(member)          # Update teams list
            else:
                updated_class.remove(member)        # In this case, the member was in the class and still is in the class.

        # Add members who have added the class
        for member in updated_class:
            team = self.get_new_team()
            self.add_members(team, [member])
            inverted_teams[member] = team

        fileIO.dump_teamslist(teams)
        fileIO.dump_inverted_teams(inverted_teams)
            
    # Param:
    #   org: PyGitHub organization object
    # Iterates over all teams in the organization & deletes them.
    def del_git_teams(self):
        teams = get_remote_teams(self.org)
        log2email = fileIO.load_login_to_email()
        emails = []

        for team in teams:
            members = team.get_members()
            for member in members:
                contact = log2email[member.login]
                msg = "You have been removed from {}.".format(team.name)
                emails.append({"receiver": contact, "subject": team.name, "message": msg})
                team.remove_from_members(member)
            print "Deleting team " + team.name
            team.delete()

        fileIO.dump_emails(emails)
        subprocess.call(["python", "./gmail/draft.py"])

    # Param:
    #   team: name of a team on GitHub
    #   member: name of a member of the organization
    # Purpose:
    #   Add member to team
    def add_members(self, team, members):
        teams = {t.name: t.id for t in self.org.get_teams()}
        if team in teams:
            team = self.org.get_team(teams[team])
        else:
            team = self.org.create_team(team)
        for member in members:
            team.add_to_members(self.hub.get_user(member))

    # Param:
    #   team: name of a team on GitHub
    #   member: name of a member of the organization
    # Purpose:
    #   Remove member from team
    def del_members(self, team, members):
        teams = {t.name: t.id for t in self.org.get_teams()}
        team = self.org.get_team(teams[team])
        for member in members:
            team.remove_from_members(self.hub.get_user(member))
        members = [m for m in team.get_members()]
        if members == []:
            team.delete()

    # Uses init_usernames.sh to establish a repo cloning https://github.com/Klortho/get-github-usernames.git
    # * Installs npm to permit the repo's use.
    # * Copies config/users.txt into that folder to inform the tool what github emails are boeing used.
    # * Calls node ./index.js to create dummy commits for each user identified by email.
    #   * Github maps the command-line git commits' emails to Github users.
    # Uses pygithub to create a new repo on Github.
    # Use gitpython to push the dummy repo to Github.
    # Uses pygithub to comb through the commits made to that repo.
    # Pull the usernames in.
    # Write the usernames to file in config/users.csv
    # Delete the github repo after getting usernames.
    # Delete the local repo.
    # Delete the cloned repo.
    def get_usernames(self):
        print("Gathering usernames.")
        subprocess.call(["./utils/init_usernames.sh"])
        print("init_usernames completed.")
        remote = self.org.create_repo("usernames")
        remote_url = self.url + "usernames"
        repo = Repo("./tmp/dummy-repo/")
        print("Init local & remote.")
        try:
            origin = repo.create_remote("usernames", self.insert_auth(remote_url))
            origin.push(refspec="{}:{}".format("master", "master"))
            print("Pushed.")
        except:
            remote.delete()
            print "ERROR creating remote."
        else:
            try:
                e = open("./config/users.txt", "r")
                emails = [email.strip() for email in e.readlines() if email.strip() != ""]
                emails.reverse()
                e.close()
                authors = [c.author.login for c in remote.get_commits()]
                login_to_email = {authors[i]: emails[i] for i in range(len(authors))}

                fileIO.dump_login_to_email(login_to_email)
                fileIO.write_classlist(authors)
                fileIO.dump_classlist(authors)

                print("Github usernames written to ./config/users.csv and ./config/users.json")
                print("JSON to match usernames to email accounts written to ./config/log_to_email.json")
            except:
                print("WARNING: GITHUB USERNAMES NOT WRITTEN.")
        try:
            remote.delete()
            shutil.rmtree("./tmp/")
            print("Working directory clean.")
        except:
            try:    
                self.org.get_repo("usernames").delete()
            except:
                pass
            print("WARNING: ./tmp/ REMAINS IN FILETREE.")

    # DISTRIBUTION METHODS
    #----------------------------------------------------------------------------------
    
    # Used to check whether an assignment has been assigned before assigning it.
    # If repos != [], then it is because there is at least one repo assigned to
    # a team for that assignment.  If that is true, then the repos have been assigned
    # in the past.
    def is_assigned(self, lab):
        repos = [r.name for r in self.org.get_repos() if lab in r.name and r.name != lab and "team" in r.name]
        return repos != []

    # Assumes that the url for the lab's repo within the organization matches the repo name
    def set_base(self, lab):
        urls = self.load_repos()
        try:
            print "Setting local clone of base code."
            base, url = self.local_clone(lab)
            if "base" in urls:
                urls["base"][lab] = url
            else:
                urls["base"] = {lab: url}
            return base
        except Exception as e:
            print "Error making local clone of base code."
            print e
            return False

    # Params:
    #   lab: identifier for the lab, eg "lab1".
    #   team: PyGitHub team object.
    #   base_repo: GitPython repo object.
    #   org: PyGitHub organization object
    # Purpose:
    #   Distributes the repo to a team from a local copy of the repo.
    # Returns:
    #   A dictionary mapping the lab identifier to the url of the team's clone.
    def remote_clone(self, lab, team, base_repo):
        base_url = self.url+lab
        repo_name = self.gen_repo_name(lab, team.name)
        team_repo = None
        try:
            team_repo = self.org.create_repo(repo_name, team_id=team, private=True)
        except:
            team_repo = self.org.create_repo(repo_name, team_id=team)
        repo_url = self.url + repo_name
        remote = base_repo.create_remote(team_repo.name, self.insert_auth(repo_url))
        remote.push(refspec="{}:{}".format("master", "master"))
        return repo_url

    # Param:
    #   lab: string identifier for a lab
    # Purpose:
    #   Creates a local copy of the lab's base code in order to distribute it to students in the class.
    # Return:
    #   GitPython Repo object
    def local_clone(self, lab):
        token = fileIO.read_token()
        url = self.url+lab
        if os.path.exists("./base/"):
            shutil.rmtree("./base/")
        base_repo = Repo.clone_from(self.insert_auth(url), "./base/")
        return base_repo, url

    def assign_repos(self, lab, base):
        teams = self.org.get_teams()
        teams = [team for team in teams if "team" in team.name]
        urls = self.load_repos()
        for team in teams:
            repos = team.get_repos()
            repos = [repo.name for repo in repos]
            lab_name = self.gen_repo_name(lab, team.name)
            try:
                print "Assigning " + team.name + " the repo."
                team_repo = self.remote_clone(lab, team, base)
                if team.name in urls:
                    urls[team.name][lab] = team_repo
                else:
                    urls[team.name] = {lab: team_repo}
            except Exception as e:
                print "Error cloning lab for " + team.name
                print e
                print "Waiting before trying again."
                sleep(5)
                try:
                    print "Assigning " + team.name + " the repo."
                    team_repo = self.remote_clone(lab, team, base) 
                    if team.name in urls:
                        urls[team.name][lab] = team_repo
                    else:
                        urls[team.name] = {lab: team_repo}
                except Exception as e:
                    print "Error cloning lab for " + team.name
                    print e
                    return False

        self.write_repos(urls)
        return True 

    # Param:
    #   org: PyGitHub organization object
    #   lab: string identifier for the base code for a lab.  Defaults to testlab1.
    # Purpose:
    #   To iterate over all the teams for the CMPUT229 GitHub organization and
    #   assign each team a clone of the repo containing the base code.
    def set_repos(self, lab):
        teams = [team for team in self.org.get_teams() if "team" in team.name]
        if teams == []:
            print "ERROR: You need to set teams (-t) before distributing repos to them!"
            return False
        print "Setting repos for {}.".format(lab)

        base = self.set_base(lab)
        if (base):
            if (self.assign_repos(lab, base)):
                pass
            else:
                print "Error assigning repos."
            shutil.rmtree("./base/")
        else:
            print "Error assigning base code."
            return False
        return True

    def distribute(self, lab):
        if self.set_repos(lab):
            try:
                self.notify_all(lab)
                self.set_hooks(lab)
                self.make_jobs_DSL(lab)
            except:
                print("ERROR: REPOS ASSIGNED, BUT NOTIFICATION, HOOKS, OR JOBS_DSL FAILED.")

    # Param:
    #   lab: String
    # Purpose:
    #   Gather all repos from all teams matching the lab
    #   Used to collect assignments
    #   Used to get local copies to submit to moss
    def get_repos(self, lab):
        print "Getting repos from GitHub."
        teams = get_remote_teams(self.org)
        teams = [team.name for team in teams in "team" in team.name]
        # teams.remove("Students")
        if not os.path.isdir("./submissions/"):
            os.mkdir("./submissions/")

        for team in teams:
            print "Getting {}'s repo.".format(team)
            url = "{}{}".format(self.url, "{}_{}".format(team, lab))
            clone_path = "./submissions/{}/{}/".format(lab, team)
            if os.path.exists(clone_path):
                shutil.rmtree(clone_path)
            Repo.clone_from(self.insert_auth(url), clone_path)
            commit = self.get_repo_by_deadline(team, lab)
            subprocess.call(["./utils/rollback.sh", clone_path, commit])
        
        base_url = "{}{}".format(self.url, lab)
        base_path = "./submissions/{}/base/".format(lab)
        if os.path.exists(base_path):
            shutil.rmtree(base_path)
        Repo.clone_from(self.insert_auth(base_url), base_path)

    # Param:
    #   Lab: Which lab/assignment will be deleted
    # Purpose:
    #   Deletes local files for lab
    def del_local_repos(self, lab="testlab1"):
        clone_path = "./submissions/{}/".format(lab)
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)

    # Param:
    #   org: PyGitHub organization object
    #   lab: string identifier for a lab.  Defaults to testlab1.
    # Purpose:
    #   Iterates over all repos for all teams in the organization and 
    #   deletes each team's repo for a given lab.
    def del_git_repos(self):
        teams = [team for team in self.org.get_teams() if "team" in team.name]
        log2email = fileIO.load_login_to_email()
        emails = []

        for team in teams:
            repos = team.get_repos()
            for repo in repos:
                name = repo.name
                print "Deleting repo " + name
                repo.delete()
                for member in team.get_members():
                    contact = log2email[member.login]
                    msg = "Your team's repo for {} has been removed.".format(name)
                    emails.append({"receiver": contact, "subject": name, "message": msg})

        fileIO.dump_emails(emails)
        subprocess.call(["python", "./gmail/draft.py"])

    # WEBHOOKS METHODS
    #----------------------------------------------------------------------------------
    def clean_hooks(self, repo):
        hooks = repo.get_hooks()
        for hook in hooks:
            if self.get_server()+"/github-webhook/" in hook.config["url"]:
                hook.delete()

    def make_hook(self, repo):
        name = "web"
        config = {"url": "https://" + self.get_server() + "/github-webhook/"}
        events = ["push"]
        active = True
        hook = repo.create_hook(name, config, events, active)        
                
    def set_hooks(self, lab):
        print "Setting webhooks."
        urls = self.load_repos()
        if "base" in urls:
            del urls["base"]
        for team,repos in urls.items():
            if lab in repos:
                repo = self.org.get_repo(self.gen_repo_name(lab, team))
                self.clean_hooks(repo)
                self.make_hook(repo)
                print "Setting webhook from {} to {}.".format(self.gen_repo_name(lab, team), self.get_server())

    # JENKINS METHODS
    #----------------------------------------------------------------------------------
    def write_jobs_repos(self, lab):
        teams = [t.name for t in self.org.get_teams()]
        teams.remove("Students")

        repos = []
        for team in teams:
            repos.append(self.gen_repo_name(lab, team))

        out = "String lab = \"{}\"\n".format(lab)
        out += "def repos = [\n"
        for r in repos:
            out += "\t\"" + r + "\",\n"
        out = out[:-2]
        out += "\n]\n"
        
        f = open("./jenkins/components/j_repos.groovy", "w")
        f.write(out)
        f.close()

    def make_jobs_DSL(self, lab):
        print "Writing a jenkins jobs file to ./jenkins/jobs.groovy"
        self.write_jobs_repos(lab)
        out = ""
        files = ["./jenkins/components/j_config.groovy", 
                 "./jenkins/components/j_repos.groovy",
                 "./jenkins/components/j_pre.groovy",  
                 "./jenkins/components/{}".format(lab),
                 "./jenkins/components/j_post.groovy"]
        for f in files:
            f = open(f, "r")
            out += f.read() + "\n"
            f.close()
        f = open("./jenkins/{}.groovy".format(lab), "w")
        f.write(out)
        f.close()


    # NOTIFICATION METHODS
    #----------------------------------------------------------------------------------

    # Param:
    #   lab: String lab
    # Purpose:
    #   to iterate over all students by team in order to notify them
    #   that the lab has been assigned.
    def notify_all(self, lab):
        teams = [team for team in self.org.get_teams() if "team" in team.name]
        urls = self.load_repos()
        log2email = fileIO.load_login_to_email()

        emails = []

        for team in teams:
            repos = [t.name for t in team.get_repos()]
            notify_repo = self.gen_repo_name(lab, team.name)
            if notify_repo in repos:
                for member in team.get_members():
                    contact = log2email[member.login]
                    url = urls[team.name][lab]
                    msg = "Starter code for {} has been distributed.  You can find this code at {}".format(lab, url)
                    emails.append({"receiver": contact, "subject": lab, "message": msg})
                    # try:
                    #    notify(contact, team.name, lab, url)
                    #    print("{} is notified that {} is distributed.".format(member.login, lab))
                    #except:
                    #    print("ERROR: SENDING THE NOTIFICATION TO {} at {} HAS FAILED.".format(member.login, contact))
            else:
                print("ERROR: YOU ARE ATTEMPTING TO NOTIFY {} ABOUT A REPO THEY HAVE NOT BEEN ASSIGNED.".format(team.name))

        fileIO.dump_emails(emails)
        subprocess.call(["python", "./gmail/draft.py"])

    # COLLECTION METHODS
    #----------------------------------------------------------------------------------
    # Params:
    #   team: string identifier for the team
    #   lab: string identifier for the lab
    # Purpose:
    #   Gather all commits made to a repo by the team.
    # Returns:
    #   A list of PyGitHub commit objects
    def get_commits(self, team, lab):
        name = self.gen_repo_name(lab, team)
        repo = self.org.get_repo(name)
        commits = [c for c in repo.get_commits()]
        return commits

    # Params:
    #   lab: string identifier for the lab
    # Purpose:
    #   To read the deadline for a given lab from file.
    # Returns:
    #   String Date in the format %Y-%m-%d %H:%M:%S
    def get_deadline(self, lab):
        d = fileIO.read_deadlines()

        deadlines = {}
        for line in d:
            l, date = line.split(",")
            deadlines[l] = date
        if lab in deadlines:
            return deadlines[lab].strip()
        else:
            print "You need to set a deadline for this lab in ./config/deadlines.csv"

    # Params:
    #   team: string identifier for a team
    #   lab: string identifier for a lab
    # Purpose:
    #   To identify which commit is the closest to the deadline without overstepping it.
    # Returns:
    #   unique id for the commit pre/at the deadline.
    def get_repo_by_deadline(self, team, lab):
        deadline = parse_date(self.get_deadline(lab))
        correction = timedelta(hours=6)
        deadline = deadline + correction

        print("Getting the list of commits for {}.".format(self.gen_repo_name(lab, team)))
        commits = self.get_commits(team, lab)

        # TODO: FIGURE OUT A FASTER WAY TO DO THIS.  STILL SLOW.
        print("Parsing the commits.  This is woefully slow.")
        commits = [(parse_date(str(commit.commit.author.date)),
                    commit.commit.sha)
                    for commit in commits]
        
        print("Sorting the commits.")
        commits = sorted(commits, key=lambda commit: commit[0], reverse=True)
        for commit in commits:
            if commit[0] <= deadline:
                return commit[1]        # At the very least, the first commit will be before the deadline.


    # HOUSEKEEPING METHODS
    #----------------------------------------------------------------------------------



    # Purpose:
    #   Generate a repo name given a team name and a lab/assignment name
    #   to reduce floating magic strings
    def gen_repo_name(self, lab, team):
        defaults = fileIO.load_defaults()
        if "prefix" in defaults and defaults["prefix"] != "":
            return "{}_{}_{}".format(defaults["prefix"], team, lab)
        else:
            return "{}_{}".format(team, lab)

    def get_server(self):
        defaults = fileIO.load_defaults()
        return defaults["server"]

    # Purpose:
    #   Write the team defs as csv
    #   Format: <team>,<member>\n
    def json_to_csv(self):
        f = open("./config/team_defs.json", "r")
        teams = json.load(f)
        f.close()

        out = open("./config/team_defs.csv", "w")
        for team in teams:
            for member in teams[team]:
                out.write("{},{}\n".format(team,member))
        out.close()

    # Purpose:
    #   Write the team defs as csv
    #   Format: <team>,<member>\n
    def git_to_csv(self):
        out = open("./config/team_defs.csv", "w")
        teams = get_remote_teams(self.org)
        for team in teams:
            members = [m for m in team.get_members()]
            for member in members:
                out.write("{},{}\n".format(team.name,member.login))
        out.close()

    # Purpose:
    #   Removes the local copy of the repo after distribution 
    def remove_local(self):
        shutil.rmtree("./base/")

    # Param:
    #   url: string representation of a GitHub resource.
    # Purpose:
    #   Inserts an oauth token in the url to make access easier, and to keep from committing 
    #   oauth tokens to git repos.  It lets the url remain unaltered at the higher scope.
    #   Needed for access using GitPython (different interface from PyGitHub).
    # Returns:
    #   The url, but with oauth token inserted
    def insert_auth(self, url):
        token = fileIO.read_token()
        url = url[:url.find("://")+3] + token + ":x-oauth-basic@" + url[url.find("github"):]
        return url

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

    # Purpose:
    #   To save the repos assigned to teams to file.
    def write_repos(self, urls):
        print "Writing repo urls to ./config/repos.json."
        f = open("./config/repos.json", "w")
        repos = json.dump(urls, f)
        f.close()

def parse_date(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

def save_max_team(number):
    f = open("./config/max_team.txt", "w")
    f.write(number)
    f.close()

def read_max_team():
    f = open("./config/max_team.txt", "r")
    i = f.read()
    f.close()
    return i

def get_assigned_repos():
    f = open("./config/assigned_repos.json", "r")
    repos = json.load(f)
    f.close
    return repos

# GitHub IO Functions
def get_remote_teams(org):
    return [team for team in org.get_teams() if "team" in team.name]

def get_remote_team_names(org):
    return [team.name for team in org.get_teams() if "team" in team.name]

def get_max_team(org):
    teams = [int(team.name[4:]) for team in org.get_teams() if "team" in team.name]
    if teams == []:
        return "team0"
    else:
        teams.sort()
        return "team{}".format(int(teams[-1]) + 1)

