#-------------------------------
# Author: Kristen Newbury
# Date: June 12 2017
#
#
# test case for most trivial case,
# single function call, no control flow
# one source reg and one as dst then source
#
# lives at jal foo: $s0
#
#-------------------------------

.text
main:
	addi	$sp, $sp, -4		# Adjust the stack to save $fp
	sw	$fp, 0($sp)		# Save $fp
	add	$fp, $zero, $sp		# $fp <= $sp
	addi	$sp, $sp, -4		# Adjust stack to save variables
	sw	$ra, -4($fp)		# Save $ra

    add     $s2, $zero, $zero
    add     $t2, $zero, $zero

    jal     foo

    add     $t2, $s0, $zero
    addi    $t2, $t2, 1


    lw      $ra, -4($fp)
    addi    $sp, $sp, 4
    lw      $fp, 0($sp)
    addi    $sp, $sp, 4
    jr      $ra


foo:
	addi	$t0, $zero, 13
	addi    $t2, $zero, 42
    jr      $ra
