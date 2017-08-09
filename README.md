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
This toolset uses these Python Modules at these versions:  
* GitPython, version 2.1.3
* PyGithub, version 1.34
* PyJWT, version 1.5.0
* argparse, version 1.2.1
* gitdb2, version 2.0.0
* smmap2, version 2.0.1
* wsgiref, version 0.1.2

These dependencies may be installed by the user, or if the user is concerned about conflicts with existing Python dependencies, the user may run the setup.sh bash script provided in order to setup a Python virtual environment.

## For further help with the service, please refer to the [wiki](https://github.com/cmput229/TA_classroom_manager/wiki).  
