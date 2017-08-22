#-------------------------------
# Author: Kristen Newbury
# Date: August 1 2017
#
#
# test case for max functions and max function calls (10 each)
#
# lives at jal foo0: $s0
# lives at jal foo0: $t0
# lives at jal foo0:
# lives at jal foo0: $t2
# lives at jal foo0:
# lives at jal foo0:
# lives at jal foo0:
# lives at jal foo0:
# lives at jal foo0:
# lives at jal foo0: $t1
#
#-------------------------------
.text
main:

    jal     foo0
    add     $t2, $s0, $zero
    jr      $ra

foo0:
    jal     foo0
	addi	$t0, $t0, 13
	addi    $t2, $zero, 42
    jr      $ra
foo1:
    addi	$t0, $zero, 13
    addi    $t2, $zero, 42
    jal     foo0
    jr      $ra
foo2:
    addi	$t0, $zero, 13
    jal     foo0
    addi    $t2, $t2, 42
    jr      $ra
foo3:
    jal     foo0
    addi	$t0, $zero, 13
    addi    $t2, $zero, 42
    jr      $ra
foo4:
    addi	$t0, $zero, 13
    addi    $t2, $zero, 42
    jal     foo0
    jr      $ra
foo5:
    addi	$t0, $zero, 13
    addi    $t2, $zero, 42
    jal     foo0
    jr      $ra
foo6:
    addi	$t0, $zero, 13
    addi    $t2, $zero, 42
    jal     foo0
    jr      $ra
foo7:
    addi	$t0, $zero, 13
    addi    $t2, $zero, 42
    jal     foo0
    jr      $ra
foo8:
    jal     foo0
    addi	$t0, $zero, 13
    addi    $t2, $t1, 42
    jr      $ra
