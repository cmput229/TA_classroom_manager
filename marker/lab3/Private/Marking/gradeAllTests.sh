# gradeAllTests.sh
# Author: Kristen Newbury
# Date: May 2 2017
#
#
# Adapted from:
# Author: Taylor Lloyd
# Date: June 27, 2012
#
# USAGE: ./gradeAllTests.sh STUDENTLABFILE
#
# compares student output against expected output
#
# Thus the following are testcase sample output reports that appear in the .out file:
#
# a: Pass
# b: Failed
# c: Failed
#
# Sometimes a student solution results in an exception that causes an
# infinite loop. In this case the script will automaticaly timeout
# after a few seconds and proceed to the next test case.
#
# variations of the sed command:
#
# for spim 8.0 - sed '1,5d'
#
# for spim 9.1.17 - sed '1d'
#
rm -f ${1%.s}.out ${1%.s}.pout
echo "Running tests on $1"
for f in tests/*.bin
    do
    rm -f student.out
    source runTest.sh $1 $f >> student.out
    suf=${f%.bin}
    if diff ${f%.bin}.out student.out >/dev/null; then
        echo "${suf#**\/} : Pass" >> ${1%.s}.out
        echo "${suf#**\/} : Pass" >> ${1%.s}.pout
    else
        if [ $excode -eq 124 ] ; then
            echo "${suf#**\/} : Failed - TEST HUNG" >> ${1%.s}.out
            echo "${suf#**\/} : Failed - TEST HUNG" >> ${1%.s}.pout
        else
            echo "${suf#**\/} : Failed" >> ${1%.s}.out
            echo "${suf#**\/} : Failed (Diff Below)" >> ${1%.s}.pout
            echo "========================= Expected =========================== ========================== Actual ============================" >> ${1%.s}.pout
            diff -y --left-column ${f%.bin}.out student.out >> ${1%.s}.pout
            echo "=============================================================================================================================" >> ${1%.s}.pout
        fi

    fi



    done
rm -f testBuild.s student.out
cat ${1%.s}.out

