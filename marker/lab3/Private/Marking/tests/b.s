#-------------------------------
# Author: Kristen Newbury
# Date: June 12 2017
#
#
# test case for only jumps(no branch), one live one dead
#
# lives at jal foo: $t0
# lives at jal bar: $s0
#
#-------------------------------

.text
main:
	addi	$sp, $sp, -4		# Adjust the stack to save $fp
	sw	$fp, 0($sp)		# Save $fp
	add	$fp, $zero, $sp		# $fp <= $sp
	addi	$sp, $sp, -4		# Adjust stack to save variables
	sw	$ra, -4($fp)		# Save $ra


    jal     foo
    add     $t2, $zero, $zero

    j       skipCode

    addi    $t0, $t1, 1
    add     $t2, $t2, $t0

skipCode:

    add     $t0, $t0, $zero
    addi    $t1, $zero, 100
    addi    $s7, $zero, -9

    lw      $ra, -4($fp)
    addi    $sp, $sp, 4
    lw      $fp, 0($sp)
    addi    $sp, $sp, 4
    jr      $ra


foo:
	addi	$t0, $zero, 13
	addi    $t2, $zero, 42
    jal     bar

    add     $t2, $s0, $zero

    j       skipCodeAgain

    addi    $t0, $s2, 1
    add     $t2, $t2, $t0

skipCodeAgain:

    add     $t0, $s0, $zero
    addi    $t1, $zero, 100
    addi    $s0, $zero, -9
    jr      $ra
bar:
    addi	$t8, $zero, 1
    addi    $t9, $zero, 4
    jr      $ra
