#-------------------------------
# Author: Kristen Newbury
# Date: June 12 2017
#
#
# test case for only branches(no jump),
# one live on one path and dead on other path
#
# lives at jal foo: $t0 $t1 $s1
# lives at jal bar: $s7
# lives at jal other: $t6
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

addi    $s1 $s1 1
bgtz    $t1 aBranch

addi    $t1 $t0 1

aBranch:
addi    $t0 $t1 1


jal     bar
add     $s7 $s7 $s7
add     $t6 $zero $s7

jal     other
add     $t0 $t6 $zero
add     $t7 $t0 $zero


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
    addi	$t0, $zero, 13
    addi    $t2, $zero, 42
    jr      $ra
other:
    addi	$t0, $zero, 13
    addi    $t2, $zero, 42
    jr      $ra

