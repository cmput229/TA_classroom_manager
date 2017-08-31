String c = '41fa261c-da80-4158-9f7f-310460627d64'
String org = "GitHubClassroomTestCMPUT229/"

String lab = "lab3"
def repos = [
	"team0_lab3",
	"team1_lab3",
	"team2_lab3"
]

repos.each {
  String name = it
  job(name) {
    scm {
      git {
        remote {
          github(org + name)
          branch('master')
          credentials(c)
        }
        configure { node ->
          node / "extensions" << "hudson.plugins.git.extensions.impl.MessageExclusion" {
            excludedMessage "(?s)^Jenkins.*"
            wipeOutWorkspace
          }
        }
      }
    }
    triggers {
      githubPush()
    }


    steps {
      shell("git checkout master")
      shell("git pull")

      shell("cp ~/grader/lab3/runTest.sh ./")
      shell("cp ~/grader/lab3/testfile.bin ./")
      shell("cp ~/grader/lab3/common.s ./")

      shell("bash ~/grader/setup.sh")
      shell("bash ./runTest.sh ./lab3.s ./testfile.bin > ./Jenkins/\"\$BUILD_TIMESTAMP\"")

      shell("rm ./runTest.sh")
      shell("rm ./testfile.bin")
      shell("rm ./common.s")
      shell("rm ./testBuild.s")

      shell("git add .")
      shell("git commit -m 'Jenkins CI Response'")
    }

    configure { node ->
      node / "publishers" << "hudson.plugins.git.GitPublisher" {
        configVersion "2"
        pushMerge "True"
        forcePush "True"
        branchesToPush {
          "hudson.plugins.git.GitPublisher_-BranchToPush" {
            targetRepoName "origin"
            branchName "master"
          }
        } 
      }
    }
  }
}

