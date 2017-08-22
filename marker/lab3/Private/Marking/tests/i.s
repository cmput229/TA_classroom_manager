#-------------------------------
# Author: Kristen Newbury
# Date: June 12 2017
#
#
# test case for case with most complex control flow
#
# lives at jal foo: $t1 $t5 $s0 $t9
# lives at jal bar: $t1 $t5 $s0 $t8 $t9
# lives at jal last: $t8
#
#-------------------------------
.text
main:
	addi	$sp, $sp, -4		# Adjust the stack to save $fp
	sw	$fp, 0($sp)		# Save $fp
	add	$fp, $zero, $sp		# $fp <= $sp
	addi	$sp, $sp, -4		# Adjust stack to save variables
	sw	$ra, -4($fp)		# Save $ra

begin:
    andi    $t9 $zero 1
    andi    $t5 $zero 1
    add     $t2, $zero, $zero
    addi    $t1  $zero 5
    addi    $s0, $zero, 1

    jal     foo
    addi    $t8 $zero 1
    beq     $t1 $zero oneForward

oneBack:
    addi    $t1 $t1 -1
    beq     $t1 $s0 almostDone
    add     $t3 $t5 $t1

oneForward:
    addi    $t5 $zero 1
    jal     bar
almostDone:
    beq     $t5 $t9 oneBack

    addi    $t0 $zero 1
    add     $t3 $s0 $t1

    jal     last
    beq     $t8 $zero begin

    lw      $ra, -4($fp)
    addi    $sp, $sp, 4
    lw      $fp, 0($sp)
    addi    $sp, $sp, 4
    jr      $ra


foo:
	addi	$t0, $zero, 13
	addi    $t2, $zero, 42
    jr      $ra
bar:
    addi	$t8, $zero, 43
    addi    $t9, $zero, 12
    jr      $ra
last:
    addi	$t1, $zero, 0
    addi    $t1, $t1, 12
    jr      $ra
