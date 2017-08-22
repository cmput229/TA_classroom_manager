# buildExpectedOutput.sh
# Author: Kristen Newbury
# Date: June 12 2017
#
#
# Adapted from:
# Author: Taylor Lloyd
# Date: June 27, 2012
#
#
# USAGE: ./buildExpectedOutput.sh
#
# builds the expected output for the solution on all tests
#
# variations of the sed command:
#
# for spim 8.0 - sed '1,5d'
#
# for spim 9.1.17 - sed '1d'
#


for f in tests/*.bin
do
rm -f ${f%.bin}.out
echo "Running $f:"
./runTest.sh ../Solution/findLiveSolution.s $f >> ${f%.bin}.out  #may need alteration
done
rm -f testBuild.s

