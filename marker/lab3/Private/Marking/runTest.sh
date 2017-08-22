# runTest.sh
# Author: Kristen Newbury
# Date: May 2 2017
#
#
# Adapted from:
# Author: Taylor Lloyd
# Date: June 27, 2012
#
#
# USAGE: ./runTest.sh LABFILE TESTFILE
#
# Combines the lab, test, and common execution file,
# then runs the resulting creation. All output generated
# is presented on standard output, after discarding the
# standard SPIM start message, which displays version
# info and could otherwise break tests.
#
# variations of the sed command:
#
# for spim 8.0 - sed '1,5d'
#
# for spim 9.1.17 - sed '1d'
#

rm -f testBuild.s
cat common.s > testBuild.s
cat $1 >> testBuild.s
# Timeout will automatically weed out hangs.
timeout 1 sh -c "spim -file testBuild.s $2 | sed '1d'"       #may need alteration
excode=$?
