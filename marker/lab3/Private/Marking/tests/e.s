#-------------------------------
# Author: Kristen Newbury
# Date: August 1 2017
#
#
# test case for correct save instruction parsing
#
# lives at jal foo: $s0 $s1 $s2 $s4 $s5 $s7
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

    sw      $s0 0($s1)
    sh      $s4 0($s2)
    sb      $s5 0($s7)


    lw      $ra, -4($fp)
    addi    $sp, $sp, 4
    lw      $fp, 0($sp)
    addi    $sp, $sp, 4
    jr      $ra


foo:
	addi	$t0, $zero, 13
	addi    $t2, $zero, 42
    jr      $ra
