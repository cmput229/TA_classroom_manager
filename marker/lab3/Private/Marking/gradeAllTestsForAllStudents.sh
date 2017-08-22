# Author: Kristen Newbury
# Date: May 19 2017
#
# Adapted from:
# gradeAllTestsForAllStudents.sh
# Author: Taylor Lloyd
# Date: July 4, 2012
#
# USAGE: ./gradeAllTestsForAllStudents.sh DIRECTORY_WITH_STUDENTS_SOLUTIONS
#
# Loops through all testfiles in the tests folder,
# calling runTest on each of them. Execution results
# are then compared to expected results, and each test
# reports as Passed or Failed.

for f in $1/*.s
    do
    rm -f ${f%.bin}.outpath ${f%.bin}.out
    ./gradeAllTests.sh $f
done
