from classroom_manager import Manager
import moss

def main():
    org_name = ""
    repo_name = ""
    arch_name = ""
    args = sys.argv

    if "-h" in args:
        print """--------------------------------------------------------------------
This is a list of flags on the command-line:

-o <organization_name>: set organization name           ([o]rg set)
-r <repo_name>: set repo for script                     ([r]epo set)
-t: set teams for the organization locally              ([t]eams set)
-a <team_name> <member>: Add <member> to <team>         ([a]dd member)
-d <team_name> <member>: delete <member> from <team>    ([d]emove member)
-s: distribute base repo (-r <repo>) to teams on GitHub ([s]et repos)
-n: notify students of repo distribution                ([n]otify)
-g: collect repos (-r <base_repo>) from students        ([g]et repos)
-m: mark repos
-c: compare repos using MOSS
-x: clear local repos (-r <assignment>)
-X: clear teams & repos on GitHub
--------------------------------------------------------------------
"""

    if "-o" in args:
        i = args.index("-o")+1
        org_name = args[i]
        i += 1
        while i < len(args) and args[i][0] != "-":
            org_name += " {}".format(args[i])     # Set org name
            i += 1
        update("org", org_name)
    else:
        if defaults():
            org_name = defaults()["org"]
        else:
            return 1

    m = Manager(org_name)

    if "-t" in args:
        m.set_teams()                           # local
        m.set_git_teams()                       # remote
        m.git_to_csv()                          # setup csv for teams

    if "-a" in args:
        team = args[args.index("-a")+1]
        start = args.index("-a")+2
        end = start
        while end < len(args):
            if args[end][0] == "-":
                break
            end += 1
        members = args[start:end]               # set members
        args = args[:start-2] + args[end:]
        m.add_members(team, members)

    if "-d" in args:
        team = args[args.index("-d")+1]
        start = args.index("-d")+2
        end = start
        while end < len(args):
            if args[end][0] == "-":
                break
            end += 1
        members = args[start:end]
        args = args[:start-2] + args[end:]      # set members
        m.del_members(team, members)

    if "-r" in args:
        repo_name = args[args.index("-r")+1]    # Set lab name
        update("repo", repo_name)
    else:
        if defaults():
            repo_name = defaults()["repo"]
        else:
            return 1
    
    if "-s" in args:
        m.set_repos(repo_name)                  # Set github repos
    
    if "-n" in args:
        m.notify_all(repo_name)
        return

    if "-A" in args:
        arch_name = args[args.index("-A")+1]

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
