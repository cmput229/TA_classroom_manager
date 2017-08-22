#-------------------------------
# Author: Kristen Newbury
# Date: June 12 2017
#
#
# test case for knownToBeDead handling
# multiple branches in a row, one dead above all
#
# at jal foo: save $t0 $t2
# at jal bar: save $t1 $t2 $s4 $t8
#
#-------------------------------

.text
main:
addi	$sp, $sp, -4		# Adjust the stack to save $fp
sw	$fp, 0($sp)		# Save $fp
add	$fp, $zero, $sp		# $fp <= $sp
addi	$sp, $sp, -4		# Adjust stack to save variables
sw	$ra, -4($fp)		# Save $ra


add     $t2, $zero, $zero
addi    $t1  $zero 5
addi    $t0, $zero, 1

jal     foo
addi    $t1 $t2 1
beq     $zero $zero branchOne
j       allDone

branchOne:
addi    $t7 $t2 1
beq     $t0 $t7 branchTwo
j       allDone

branchTwo:
beq     $t0 $t7 branchThree
j       allDone

branchThree:
addi    $t0 $t1 1

allDone:

lw      $ra, -4($fp)
addi    $sp, $sp, 4
lw      $fp, 0($sp)
addi    $sp, $sp, 4
jr      $ra


foo:
    addi	$t0, $zero, 13
    addi    $t7, $zero, 42
    jal     bar
    addi    $t8 $t8 1
    addi    $s5 $t8 1
    beq     $t2 $t8 branchFour
    j       fooDone

branchFour:
    addi    $t4 $t8 1
    beq     $t8 $t2 branchFive

branchFive:
    addi    $s4 $s4 1
    addi    $s4 $s5 1
    beq     $t4 $t4 branchSix
    j       fooDone

branchSix:
    addi    $t0 $t1 1
fooDone:
    jr      $ra
bar:
    addi	$t0, $zero, 13
    addi    $t2, $zero, 42
    jr      $ra
