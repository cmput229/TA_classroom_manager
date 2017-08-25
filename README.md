## For further help with the service, you may refer to the [wiki](https://github.com/cmput229/TA_classroom_manager/wiki).  

# Classroom Manager
A repo to hold all the tools being developed.

This set of tools can be used to:  
- Distribute assignment starter code to students as private repos belonging to a GitHub organization.
- Provide continuous integration to students with Jenkins.
- Associate webhooks with the repos assigned to students in order to trigger Jenkins pulls.
- Collect repositories up to a deadline for each assignment.
- Compare student source code using Stanford's Moss.
- Gather local copies of Moss's feedback.
- Automate grading of assignments using a modified version of Owen Stenson's spimgrader.
- Collate results for the class's assignments as .csv files.

# Requirements
This toolset is designed to work with Python 2.7+.

In order to run setup.sh, you will require Virtualenv to be installed.
* [virtualenv](https://virtualenv.pypa.io/en/stable/)  

The module responsible for gathering usernames requires npm and nodejs-legacy to be installed.  
(This will be handled automatically by ./setup.sh)  
* [npm](https://www.npmjs.com/)
* [node](https://nodejs.org/en/)

To use gmail to send notifications, the Google Client Library needs to be installed in ./gmail/.  
(This will be handled automatically by ./setup.sh)  
* [gmail API quickstart](https://developers.google.com/gmail/api/quickstart/python)  

This toolset uses these Python Modules at these versions:  
* GitPython, version 2.1.3
* PyGithub, version 1.34
* PyJWT, version 1.5.0
* argparse, version 1.2.1
* gitdb2, version 2.0.0
* smmap2, version 2.0.1
* wsgiref, version 0.1.2

These dependencies may be installed by the user, or if the user is concerned about conflicts with existing Python dependencies, the user may run the setup.sh bash script provided in order to setup a Python virtual environment.

# Instructions
There are two main parts to the service.  I) The toolset II) The Jenkins Server.  

# Setup for the toolset
1. Obtain access to the GitHub organization https://github.com/cmput229.
2. Clone the repo https://github.com/cmput229/TA_classroom_manager into a convenient folder.
3. Obtain an OAuth token for the organization that will be hosting the starter code, as per https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/.
    3a. Store the token in the root of the toolset directory in a file called git.token.
4. Obtain an OAuth token for Google's Gmail, as per https://developers.google.com/gmail/api/quickstart/python.
    4a. Store the token in the root of the toolset directory in a file called client_secret.json.
5. In the repo folder, run ./setup.sh.  This will create a virtual environment for Python, install the dependencies needed to run the tools, and authenticate with Google using client_secret.json.
    5a.  A browser window should open as it validates with Google.  You will need to interact with the window in order to grant permission for the application to use the Gmail account associated with the service account for the organization.
6. The script will finish running and deactivate the virtual environment.
7. Activate the virtual environment by typing "source venv/bin/activate"
8. Indicate the organization that will be used by typing <toolset_path>/main.py -O <organization_name> on the commandline.
9.  Initial setup is complete for the toolset.

# Setup for the Classroom
OPTION 1: After LDAP
1.  Must happen after a class list has been obtained, and students have joined the class's organization.  Assumes that a list of ualberta emails for the class has been obtained and stored as users.txt in <toolset>/config.  Assumes that teams are defined (if needed) in <toolset>/config/teams.csv.
OPTION 2: Manually Create List - mostly for testing
1.  Add emails to file <toolset>/config/users.txt

2.  Specify a prefix for the term, if desired, by running <toolset>/main.py -P <prefix>
2.  Run <toolset>/main.py -t to setup teams.
3.  Teams will be defined within the GitHub organization.  Setup for the classroom is complete.

# Distribute a Repo
1.  Identify the repo to be distributed to the students by typing <toolset>/main.py -R <repo_name>.  The repo needs to be hosted within the organization. 
2.  Distribute the repo to the teams on the organization by typing <toolset>/main.py -d
2a.  This distributes repos, sets webhooks, and sends notifications.
3.  The repo will be distributed to each team.  Each member of each team will be notified by email that the repo has been assigned.  A url to their clone of the repo will be provided in the repo.

# Collect Repos
1.  Identify the repo to be be collected by the toolset by typing <toolset>/main.py -R <repo_name> (If needed; the repo may still be the same and the change might not be necessary).  Assumes that the deadline for the asignment is defined in <toolset>/utils/deadlines.csv.2.  Collect the repo by typing <toolset>/main.py -f
2a.  This makes local clones of the repos in <toolset>/submissions/<lab>/<team>/ for each team working on that lab, applies the autograder scripts to the labs, generates a summary file in <toolset>/marker/summary/<lab>.csv, and sends the student submissions off to MOSS to be compared.  After MOSS has finished, a local copy is made of the results.
3.  Collection has finished.

# Clear the Organization
1. Type <toolset>/main.py -X to clear all teams and repos from the organization.
1a. You will be prompted before it continues to do that.

# Setup for the Jenkins Server
1.  Setup a Jenkins Server in such a way that it is accessible to other computers.
2.  Install the following plugins as part of the setup.
    - default plugins
    - Git Plugin
    - Jobs DSL Plugin
    - Build Timestamp Plugin
    - Workspace Cleanup Plugin
3. Place the files that will be needed to perform continuous integration in <Jenkins_path>/grader/<lab_name>/
    eg: Files to grade public test cases for Find_Live placed in <Jenkins_path>/grader/Find_Live/
4. Inital setup is complete for the Jenkins Server.
5. Register the server's address with the toolset by typing <toolset>/main.py -S <Server_name>

# Setup Jenkins Server for Continuous Integration
1. After distributing the repo to students, Jenkins will need to be told how to handle webhook notifications about these repos.   Distribution creates a file, <toolset>/jenkins/<lab>.groovy, to describe a batch of Jenkins jobs that will need to be made in order to handle the webhooks.
    1a.  If steps need to be altered for the final jobs, those can be tweaked by changing the files located in <toolset>/jenkins/components. 
2.  Create a new freestyle Jenkins Job in the browser interface for Jenkins.
3.  Add a Build Step to the configuration for the new Job, making the step a "Process Jobs DSLs" type step.
4.  Paste the text from <toolset>/jenkins/<lab>.groovy into the text field for the Jobs DSL.
5.  Run a build of this job.
6.  New jobs will be created on the server, which are configured to listen to the repos of the students.  Setup for Jenkins CI is complete.  

## For further help with the service, please refer to the [wiki](https://github.com/cmput229/TA_classroom_manager/wiki).  
