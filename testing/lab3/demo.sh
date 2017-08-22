# Clone team0's repo
git clone https://c5836887569f2169e2d06e7630468c6f23d65720:x-oauth-basic@github.com/GitHubClassroomTestCMPUT229/team0_lab3.git ./testing/lab3/team0
# Clone team1's repo
git clone https://c5836887569f2169e2d06e7630468c6f23d65720:x-oauth-basic@github.com/GitHubClassroomTestCMPUT229/team1_lab3.git ./testing/lab3/team1
# Add lab3.s to team1's repo
rm -f ./testing/lab3/team1/lab3.s
cp ./testing/lab3/lab3.s ./testing/lab3/team1/
# Add pair.s to team0's repo and to team1's repo.
cp ./testing/lab3/pair.s ./testing/lab3/team1/
cp ./testing/lab3/pair.s ./testing/lab3/team0/

# Make commit in team0's repo & push.
cd ./testing/lab3/team0/
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
