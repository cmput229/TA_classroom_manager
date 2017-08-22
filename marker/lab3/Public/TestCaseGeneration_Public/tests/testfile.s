#-------------------------------
# Author: Kristen Newbury
# Date: June 12 2017
#
# basic test case
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

    jal     function

    add     $t2, $t0, $zero
    addi    $t2, $t2, 1
    add     $t7, $t8, $zero
    addi    $t1, $t9, 1


    lw      $ra, -4($fp)
    addi    $sp, $sp, 4
    lw      $fp, 0($sp)
    addi    $sp, $sp, 4
    jr      $ra


function:

	addi	$t0, $zero, 1
	addi    $t1, $zero, 2
    addi	$t2, $zero, 3
    addi    $t3, $zero, 4
    jr      $ra
