#-------------------------------
# Author: Kristen Newbury
# Date: June 12 2017
#
#
# test case for single branch and one jump in a loop
# one live on one path and dead on other
#
# at jal foo: save $t1 $t3 $s5
# at jal bar: save none
# at jal last: save none
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
    addi    $s5, $zero, 1

callFooLoop:
    beq     $t1 $zero doneLoop
    addi    $t1 $t3 -1
    addi    $t1 $s5 -1
    jal     foo
    add     $t2, $zero, $zero
    addi    $t0, $t2, 1
    j       callFooLoop

doneLoop:

    addi    $t0 $zero 1
    add     $t3 $t0 $t1

    jal     bar

    lw      $ra, -4($fp)
    addi    $sp, $sp, 4
    lw      $fp, 0($sp)
    addi    $sp, $sp, 4
    jr      $ra


foo:
	addi	$t0, $zero, 13
	addi    $t2, $zero, 42
    jal     last
    jr      $ra
bar:
    addi	$t3, $zero, 100
    jr      $ra
last:
    addi	$t8, $zero, -9
    jr      $ra
