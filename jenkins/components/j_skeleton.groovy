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

      shell(sprintf('%1$s %2$s', ["python ../grader/student_grader.py", lab]))
      shell(sprintf('%1$s%2$s %3$s', ["cp ../grader/diagnostics/", lab, " ./"]))

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
