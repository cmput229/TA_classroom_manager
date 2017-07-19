#!/usr/bin/env python

import json
import shutil
from github import Github
from git import Repo
from datetime import datetime
from datetime import timedelta
from time import sleep
import os
import subprocess

import spimgrader as grader
import moss
from notifier import send_notification as notify


# REFERENCE
#----------------------------------------------------------------------------------------------
# Oauth tokens in gitpython    
# http://stackoverflow.com/questions/36358808/cloning-a-private-repo-using-https-with-gitpython
# User: shawnzhu
#
# Organizations & Membership
# https://github.com/PyGithub/PyGithub/issues/507
# User: lbrownell-gpsw
#----------------------------------------------------------------------------------------------

class Manager():
    def __init__(self, name):
        self.name = name
        self.url = "https://github.com/{}/".format(name)
        token = self.get_token()
        self.hub = Github(token)        
        self.org = self.hub.get_organization(name)

    # Purpose:
    #   Generate a repo name given a team name and a lab/assignment name
    #   to reduce floating magic strings
    def gen_name(self, lab, team):
        f = open("./config/defaults.json", "r")
        defaults = json.load(f)
        f.close()
        if "prefix" in defaults and defaults["prefix"] != "":
            return "{}_{}_{}".format(defaults["prefix"], team, lab)
        else:
            return "{}_{}".format(team, lab)

    def get_server(self):
        f = open("./config/defaults.json", "r")
        defaults = json.load(f)
        f.close()
        return defaults["server"]

    # Purpose:
    #   Reads git.token to get the oauth token that allows PyGithub and GitPython 
    #   to perform their actions.
    def get_token(self):
        f = open("git.token", "r")
        token = f.readline().strip()
        return token

    # Params:
    #   hub: PyGitHub github object
    #   name: the name of the organization being retrieved
    # Purpose:
    #   Get access to the PyGitHub abstraction of the classroom
    # Returns:
    #   An instance of PyGitHub abstraction of the GitHub service
    def get_org(self):
        return self.hub.get_organization(self.name)

    # Params:
    #   hub: PyGitHub github object
    #   org: PyGitHub organization object
    # Purpose:
    #   To iterate over all the GitHub IDs in a class.txt file
    #   and add the GitHub users to the organization's membership.
    # N.B.: class.txt is a text file with student gitIDs on each line
    def set_members(self):
        class_list = open("./config/class.txt", "r")
        c = [line.strip() for line in c]
        class_list.close()

        for student in c:
            self.org.add_to_public_members(self.hub.get_user(student))

    # Default: Each student in the class is in their own team
    # Nondefault:   If students are allowed to form groups, then their groups should
    #               be identified in teams.txt
    # Should check that students are not member of more than one group.
    # class.txt is a text file with student gitIDs on each line
    # teams.txt is a text file that identifies which student gitIDs are proposed
    # to be group members.  Groups should be in csv format.
    @staticmethod
    def set_teams():
        print "Parsing class & team files."
        teams = {}
        class_list = open("./config/class.csv", "r")
        teams_list = open("./config/teams.csv", "r")
        t = teams_list.readlines()
        c = class_list.read()
        t = [line.strip().split(",") for line in t]
        c = c.strip().split(",")
        class_list.close()
        teams_list.close()

        i = 0
        for team in t:
            team_name = "team" + str(i)
            teams[team_name] = team
            i += 1
            for member in team:
                if member in c:
                    c.remove(member)

        for line in c:
            line = line.strip()
            team_name = "team" + str(i)
            teams[team_name] = [line]
            i += 1

        out = open("./config/team_defs.json", "w")
        json.dump(teams, out)
        out.close()

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
        teams = self.get_git_teams()
        for team in teams:
            members = [m for m in team.get_members()]
            for member in members:
                out.write("{},{}\n".format(team.name,member.login))
        out.close()

    # Params:
    #   hub: PyGitHub github object
    #   org: PyGitHub organization object
    # Purpose:
    #   To iterate over all the teams defined locally with ten_defs.json
    #   and create teams on GitHub.
    def set_git_teams(self):
        print "Setting teams on GitHub."

        f = open("./config/team_defs.json", "r")
        teams = json.load(f)
        f.close()

        for team in teams.keys():
            t = None
            try:
                t = self.org.create_team(team)
                print "Created " + team + " on GitHub."
            except:
                print "Error creating team: team {} already exists.".format(team)
            for member in teams[team]:
                t.add_to_members(self.hub.get_user(member))
    
    # Purpose:
    #   Gets the PyGitHub teams
    def get_git_teams(self):
        results = [team for team in self.org.get_teams()]
        return results

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

    def assign_repos(self, lab, base):
        teams = self.org.get_teams()
        urls = self.load_repos()
        for team in teams:
            if team.name != "Students":
                try:
                    print "Assigning " + team.name + " the repo."
                    team_repo = self.clone(lab, team, base)
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
                        team_repo = self.clone(lab, team, base) 
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

    def set_config(self):
        return  {"url": "https://" + self.get_server() + "/github-webhook/"}

    def clean_hooks(self, repo):
        hooks = repo.get_hooks()
        for hook in hooks:
            if self.get_server() in hook.config["url"]:
                hook.delete()

    def make_hook(self, repo):
        name = "web"
        config = self.set_config()
        events = ["push"]
        active = True
        hook = repo.create_hook(name, config, events, active)        
                
    def set_hooks(self, lab):
        urls = self.load_repos()
        if "base" in urls:
            del urls["base"]
        for team,repos in urls.items():
            if lab in repos:
                repo = self.org.get_repo(self.gen_name(lab, team))
                self.clean_hooks(repo)
                self.make_hook(repo)

    # Param:
    #   org: PyGitHub organization object
    #   lab: string identifier for the base code for a lab.  Defaults to testlab1.
    # Purpose:
    #   To iterate over all the teams for the CMPUT229 GitHub organization and
    #   assign each team a clone of the repo containing the base code.
    def set_repos(self, lab):
        print "Setting repos for {}.".format(lab)

        base = self.set_base(lab)
        if (base):
            if (self.assign_repos(lab, base)):
                if (self.set_hooks(lab)):
                    print "Base code, repos, and webhooks assigned and set."
                else:
                    print "Error setting webhooks."
            else:
                print "Error assigning repos."
            shutil.rmtree("./base/")
        else:
            print "Error assigning base code."


    # Param:
    #   lab: String
    # Purpose:
    #   Gather all repos from all teams matching the lab
    #   Used to collect assignments
    #   Used to get local copies to submit to moss
    def get_repos(self, lab):
        print "Getting repos from GitHub."
        teams = self.get_git_teams()
        teams = [team.name for team in teams]
        teams.remove("Students")
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
    #   lab: String lab
    # Purpose:
    #   to iterate over all students by team in order to notify them
    #   that the lab has been assigned.
    def notify_all(self, lab):
        teams = self.org.get_teams()
        urls = self.load_repos()

        for team in teams:
            if team.name != "Students":
                for member in team.get_members():
                    contact = member.email
                    if contact != None:
                        print "{} is notified that {} is distributed.".format(member.login, lab)
                        url = urls[team.name][lab]
                        notify(contact, team.name, lab, url)
                    else:
                        print "{} does not have their public email set.".format(member.login)

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
        teams = self.org.get_teams()
        for team in teams:
            repos = team.get_repos()
            for repo in repos:
                print "Deleting repo " + repo.name
                repo.delete()

    # Param:
    #   org: PyGitHub organization object
    # Iterates over all teams in the organization & deletes them.
    def del_git_teams(self):
        teams = self.org.get_teams()
        for team in teams:
            if team.name != "Students":
                members = team.get_members()
                for member in members:
                    team.remove_from_members(member)
                print "Deleting team " + team.name
                team.delete()

    # Params:
    #   lab: identifier for the lab, eg "lab1".
    #   team: PyGitHub team object.
    #   base_repo: GitPython repo object.
    #   org: PyGitHub organization object
    # Purpose:
    #   Distributes the repo to a team from a local copy of the repo.
    # Returns:
    #   A dictionary mapping the lab identifier to the url of the team's clone.
    def clone(self, lab, team, base_repo):
        base_url = self.url+lab
        repo_name = "{}_{}".format(team.name, lab)
        repo_url = self.url + repo_name
        team_repo = self.org.create_repo(repo_name, team_id=team)
        remote = base_repo.create_remote(team_repo.name, self.insert_auth(repo_url))
        remote.push()  
        return repo_url

    # Param:
    #   lab: string identifier for a lab
    # Purpose:
    #   Creates a local copy of the lab's base code in order to distribute it to students in the class.
    # Return:
    #   GitPython Repo object
    def local_clone(self, lab):
        token = self.get_token()
        url = self.url+lab
        if os.path.exists("./base/"):
            shutil.rmtree("./base/")
        base_repo = Repo.clone_from(self.insert_auth(url), "./base/")
        return base_repo, url

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
        token = self.get_token()
        url = url[:url.find("://")+3] + token + ":x-oauth-basic@" + url[url.find("github"):]
        return url

    # Purpose:
    #   To read the repos assigned to teams from file.
    def load_repos(self):
        f = open("./config/repos.json", "r")
        repos = json.load(f)
        f.close()
        return repos

    # Purpose:
    #   To save the repose assigned to teams to file.
    def write_repos(self, urls):
        f = open("./config/repos.json", "w")
        repos = json.dump(urls, f)
        f.close()

    # Params:
    #   team: string identifier for the team
    #   lab: string identifier for the lab
    # Purpose:
    #   Gather all commits made to a repo by the team.
    # Returns:
    #   A list of PyGitHub commit objects
    def get_commits(self, team, lab):
        name = "{}_{}".format(team, lab)
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
        deadlines_file = open("./config/deadlines.csv", "r")
        d = deadlines_file.readlines()
        deadlines_file.close()

        if "\n" in d:
            d.remove("\n")

        deadlines = {}
        for line in d:
            l, date = line.split(",")
            deadlines[l] = date
        return deadlines[lab].strip()

    # Params:
    #   team: string identifier for a team
    #   lab: string identifier for a lab
    # Purpose:
    #   To identify which commit is the closest to the deadline without overstepping it.
    # Returns:
    #   unique id for the commit pre/at the deadline.
    def get_repo_by_deadline(self, team, lab):
        # TODO: GitHub timestamps are at a different time than local.  Ensure that the math
        #       to get correct timestamp is correct.
        deadline = datetime.strptime(self.get_deadline(lab), "%Y-%m-%d %H:%M:%S")
        correction = timedelta(hours=6)
        deadline = deadline + correction

        commits = self.get_commits(team, lab)           
        commit = commits[-1]
        max_date = datetime.strptime(str(commit.commit.author.date), "%Y-%m-%d %H:%M:%S")
        assert(max_date < deadline)

        for c in commits:
            date = datetime.strptime(str(c.commit.author.date), "%Y-%m-%d %H:%M:%S")
            if date <= deadline and date > max_date:
                commit = c
                max_date = datetime.strptime(str(commit.commit.author.date), "%Y-%m-%d %H:%M:%S")
            else:
                pass

        return commit.commit.sha

