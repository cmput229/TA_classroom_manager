# Clone team0's repo
git clone https://c5836887569f2169e2d06e7630468c6f23d65720:x-oauth-basic@github.com/GitHubClassroomTestCMPUT229/team0_lab1.git ./testing/lab1/team0
# Clone team1's repo
git clone https://c5836887569f2169e2d06e7630468c6f23d65720:x-oauth-basic@github.com/GitHubClassroomTestCMPUT229/team1_lab1.git ./testing/lab1/team1
# Add lab1.s to team1's repo
rm -f ./testing/lab1/team1/lab1.s
cp ./testing/lab1/lab1.s ./testing/lab1/team1/
# Add pair.s to team0's repo and to team1's repo.
cp ./testing/lab1/pair.s ./testing/lab1/team1/
cp ./testing/lab1/pair.s ./testing/lab1/team0/

# Make commit in team0's repo & push.
cd ./testing/lab1/team0/
git add .
git commit -m "DEMO commit."
git push

# Make commit in team1's repo & push.
cd ../team1/
git add .
git commit -m "DEMO commit."
git push

# Clean up the workspace
cd ../
rm -rf team0
rm -rf team1

# Watch the fireworks.

cd ../../
