#-------------------------------
# Author: Kristen Newbury
# Date: August 1 2017
#
#
# test case for correct parsing of all branch types
#
# lives at jal foo: $t0 $t1 $t3 $s0 $s1 $s2 $s7 $t9
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

    beq     $t0 $s0 done
    bne     $t1 $s1 done
    bgez    $s7 done
    bgtz    $s2 done
    bltz    $t3 done
    blez    $t9 done

done:
    lw      $ra, -4($fp)
    addi    $sp, $sp, 4
    lw      $fp, 0($sp)
    addi    $sp, $sp, 4
    jr      $ra


foo:
	addi	$t0, $zero, 13
	addi    $t2, $zero, 42
    jr      $ra
