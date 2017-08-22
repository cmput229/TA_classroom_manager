import shutil
import os
import subprocess

# Traverse the collected repos, and move the .s files into a single directory.
# Rename the files during move to reflect the team, since we need to match to 
# groups for grading output.
# Takes the name of the lab / assignment as a parameter.
# Expects files in ./submissions/<lab>/<team>/
# Must expect files to be *.s for gradeAllTests.sh
# Must move files into single, shallow directory.
# Must return path to that directory (for use with call to gradeAllTests.sh).
def gather_for_marking(lab):
    dest = "./marker/{}/Private/Marking/gathered/".format(lab)
    if not os.path.isdir(dest):
        os.mkdir(dest)
    else:
        shutil.rmtree(dest)
        os.mkdir(dest)

    teams = os.listdir("./submissions/{}/".format(lab))
    teams.remove("base")
    print teams
    for team in teams:
        files = os.listdir("./submissions/{}/{}/".format(lab, team))
        for file in files:
            if file[-2:] == ".s":
                shutil.copy("./submissions/{}/{}/{}".format(lab, team, file), "{}/{}".format(dest, team+".s"))
    
    return dest[:dest.find("gathered/")]

# Must call gradeAllTestsForAllStudents.sh on the contents of the source folder.
# Source folder is assumed to be generated by gather_for_marking.
def grade(path):
    os.chdir(path)
    subprocess.call(["bash",
                     "./gradeAllTestsForAllStudents.sh", 
                     "./gathered"])

if __name__ == "__main__":
    path = gather_for_marking("lab3")
    grade(path)