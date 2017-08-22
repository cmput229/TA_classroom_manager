# runAllTests.sh
# Author: Kristen Newbury
# Date: June 15 2017
#
#
# Adapted from:
# Author: Taylor Lloyd
# Date: June 27, 2012
#
# USAGE: ./runAllTests.sh YOURLABFILE
#

rm -f all.out
echo "Running tests on $1"
for f in tests/*.bin
    do

    printf "###############################################\n" >> all.out
    echo "Running $f:" >> all.out
    printf "\n" >> all.out
    source runTest.sh $1 $2 $f >> all.out
    printf "\n" >> all.out

    done
printf "###############################################\n" >> all.out

cat all.out

