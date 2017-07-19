String c = '41fa261c-da80-4158-9f7f-310460627d64'
String org = "GitHubClassroomTestCMPUT229/"

def repos = [
	"team0_Lab_Template",
	"team1_Lab_Template"
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
      shell("python hello.py >> tmp")
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

