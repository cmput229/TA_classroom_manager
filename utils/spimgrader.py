#!/usr/bin/env python
'''
This program is modified from:
SPIM Auto-grader
Owen Stenson
Grades every file in the 'submissions' folder using every test in the 'samples' folder.
Writes to 'results' folder.

Source: https://github.com/stensonowen/spim-grader
Licence: GPL 2.0
'''
import os, time, re, sys
from subprocess import Popen, PIPE, STDOUT

def run(lab, fn, sample_input='\n'):
    proc = Popen(["spim", "-file", "./submissions/{}/{}/{}.s".format(lab, fn, lab)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    proc.stdin.write(sample_input)
    return proc 

def remove_header(output):
    #remove output header
    hdrs = []
    hdrs.append(re.compile("SPIM Version .* of .*\n"))
    hdrs.append(re.compile("Copyright .*, James R. Larus.\n"))
    hdrs.append(re.compile("All Rights Reserved.\n"))
    hdrs.append(re.compile("See the file README for a full copyright notice.\n"))
    hdrs.append(re.compile("Loaded: .*/spim/.*\n"))
    for hdr in hdrs:
        output = re.sub(hdr, "", output)
    return output

def gather_output(p, f):
    f = open("./marker/outputs/" + f, 'w')
    for proc in p:
        time.sleep(.1)
        if proc.poll() is None:
            print "Sleeping"
            #process is either hanging or being slow
            time.sleep(.5)
            if proc.poll() is None:
                print "Killing the process"
                proc.kill()
                f.write("Process hung; no results to report\n")
                continue
        output = remove_header(proc.stdout.read())
        errors = proc.stderr.read()
        if errors == "":
            f.write(output + '\n')
        else:
            f.write(output + '\t' + errors + '\n')
    f.close() 

def grade(lab, outs):
    passed = True
    diag = open("./marker/results/{}".format(outs), "w")
    outs = open("./marker/outputs/{}".format(outs), "r")
    expectations = open("./marker/expectations/{}".format(lab), "r")

    r = outs.readlines()
    e = expectations.readlines()
    assert(len(e) == len(r))
    for i in range(len(e)):
        status = "PASSED" if r[i] == e[i] else "FAILED"
        diag.write("Test Case {}:\t{}\tExpected: {}\tReceived: {}\n".format(i+1, status, e[i].strip(), r[i].strip()))
        if status == "FAILED":
            passed = False
    outs.close()
    expectations.close()
    diag.close()
    
    return passed

# ASSUMPTION: Submissions take the format "<team_name>.s".
def generate_filename(submission):
    try:
        ID = submission[:-2]
    except:
        ID = submission
    return ID

# Heads the results file with a line saying whether the tests for that file passed
def update_results(output_file, passed):
    path = "./marker/results/{}".format(output_file)
    f = open(path, "r")
    results = f.read()
    f.close()
    f = open(path, "w")
    f.write("{}{}".format(passed.__str__(), "\n"))
    f.write(results)
    f.close()

# Takes an input file that consists of a number of lines of input
# and feeds them into spim subprocesses.
def input_lines(lab):
    # ASSUMPTION: THE FILE THAT WILL BE USED TO GRADE SOME SUBMISSION
    #             WILL SHARE NAMES WITH THE SUBMISSION FILE.
    cases_path = "./marker/test_cases/{}".format(lab)
    cases_file = open(cases_path, 'r')
    cases = cases_file.readlines()
    cases_file.close()
    
    submissions = os.listdir("./submissions/{}/".format(lab))
    submissions.remove("base")

    for submission in submissions:
        print "Marking submission for {}.".format(submission)
        #cycle through samples to test:
        output_file = ""
        processes = []
        for test in cases:
            sample_input = "{}{}".format(test.strip(), "\n")
            #create process
            p = run(lab, submission, sample_input)
            processes.append(p)
        output_file = submission    # Currently submission is team_name
        gather_output(processes, output_file)
        passed = grade(lab, output_file)
        update_results(output_file, passed)

# Returns True if all tests for all files have passed; else False
def passed_all():
    path = "./marker/results/"
    files = os.listdir(path)
    files.remove(".empty")
    for f in files:
        f = open("{}{}".format(path, f), "r")
        lines = f.readlines()
        f.close()
        if lines[0].strip() == "False":
            return False
    return True

def print_results():
    path = "./marker/results/"
    files = os.listdir(path)
    for f in files:
        print "{}".format(f)
        f = open("{}{}".format(path, f), "r")
        print f.read()
        f.close()

def write_summary(lab):
    if not os.path.isdir("./marker/summary/"):
        os.mkdir("./marker/summary/")
    cases = open("./marker/test_cases/{}".format(lab), "r")
    num_case = len(cases.readlines())
    cases.close()
    teams = os.listdir("./submissions/{}/".format(lab))
    teams.remove("base")
    summary = ""
    
    for team in teams:
        num_pass = 0
        fail_str = "[ "
        f = open("./marker/results/{}".format(team), "r")
        lines = f.readlines()
        lines = lines[1:]
        for line in lines:
            if line.split("\t")[1] == "PASSED":
                num_pass += 1
            else:
                fail_str += line.split("\t")[0].split(" ")[2][:-1] + " "
        fail_str += "]"
        summary += team + "," + str(num_pass) + "/" + str(num_case) + "," + str(fail_str) + "\n"

    f = open("./marker/summary/{}.csv".format(lab), "w")
    f.write(summary)
    f.close()

# Austin intends to grade labs with a binary blob file
# TODO: Get that working.
def input_blob(test, subm, resl, diag):
    pass

def test_paths(lab):
    # No use in running if content directories aren't present.
    subm = "./submissions/{}".format(lab)
    test = "./marker/test_cases"
    expc = "./marker/expectations"
    assert os.path.isdir(subm)
    assert os.path.isdir(test)
    assert os.path.isdir(expc)
    # If we're missing other needed directories, create them.
    outs = "./marker/outputs"
    resl = "./marker/results"
    summ = "./marker/summary/"
    if not os.path.isdir(outs):
        os.mkdir(outs)
    if not os.path.isdir(resl):
        os.mkdir(resl)
    if not os.path.isdir(summ):
        os.mkdir(summ) 

# Expectation: Submission files will be  ./submissions/submission/lab<n>/<team>/
# Expectation: All test case files for lab<n> will be ./marker/test_cases/lab<n>
# Expectation: Ditto expectations file.
# Expectation: Outputs per team will be ./marker/outputs/team/Lab<n>
# Expectation: Results per team will be ./marker/results/team/Lab<n>
def main(lab, input_type="line"):
    test_paths(lab)

    print "Marking student repos."
    if input_type == "line":
        input_lines(lab)
    else:
        input_blob(lab)
    write_summary(lab)

    print "View a summary in ./marker/summary/{}.csv".format(lab)

       
if __name__ == "__main__":
    args = sys.argv
    t = None
    l = None

    if len(args) == 1:
        main()

    if "-t" in args:
        t = args[args.index("-t")+1]

    if "-l" in args:        
        l = args[args.index("-l")+1]
    
    main(l, t)

    if "-g" in args:
        if not passed_all():
            exit(1)

