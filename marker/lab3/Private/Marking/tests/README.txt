Current Test case breakdown:
(Last modified: August 1 2017)

One path tests:

a : no jumps or branches, one live register and one dead register

b : only jumps, one live register and one dead register on the path

c : one branch, x live on one path and dead on the other path

d : one branch and one jump in a loop, x live on one path and dead on the other path 

e: all save instructions present (sw, sb, sh) to test proper parsing

f: all branch instructions present (beq, bne, blez, bgez, bgtz, bltz) to test proper parsing

g: max size testing, contains 10 functions and 10 function calls

Multipath tests:

h: three successive branches : x is dead on upper path and used after the third branch (tests knownToBeDead stack/save handling)

i: edge case lots of control flow paths to follow: branches and jumps:
includes some combo of cases where regs are dead on one path and live on another   



Notes:

a is the only test to have only one function call, therefore any solution that cannot handle more than one function call will only succeed on first line of results for all testfiles. 

‘dead’ register tests as a register overwritten and then found as source.