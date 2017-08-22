#-------------------------------
# Lab- findLive
#
# Author: Kristen Newbury
# Date: June 9 2017
#
# Adapted from:
# Control Flow Lab - Student Testbed
# Author: Taylor Lloyd
# Date: July 19, 2012
#
#
#-------------------------------
.data
.align 2
binary:	  #These absolutely MUST be the first two data defined, for jump correction
.space 2052
noFileStr:
.asciiz "Couldn't open specified file.\n"
format:
.asciiz "\n"
space:
.asciiz " "
liveMessage:
.asciiz "The live registers: "
zero:
.asciiz "$0  "
at:
.asciiz "$at "
v0:
.asciiz "$v0 "
v1:
.asciiz "$v1 "
a0:
.asciiz "$a0 "
a1:
.asciiz "$a1 "
a2:
.asciiz "$a2 "
a3:
.asciiz "$a3 "
t0:
.asciiz "$t0 "
t1:
.asciiz "$t1 "
t2:
.asciiz "$t2 "
t3:
.asciiz "$t3 "
t4:
.asciiz "$t4 "
t5:
.asciiz "$t5 "
t6:
.asciiz "$t6 "
t7:
.asciiz "$t7 "
s0:
.asciiz "$s0 "
s1:
.asciiz "$s1 "
s2:
.asciiz "$s2 "
s3:
.asciiz "$s3 "
s4:
.asciiz "$s4 "
s5:
.asciiz "$s5 "
s6:
.asciiz "$s6 "
s7:
.asciiz "$s7 "
t8:
.asciiz "$t8 "
t9:
.asciiz "$t9 "

.text
main:

lw      $a0 4($a1)	# Put the filename pointer into $a0
li      $a1 0		# Read Only
li      $a2 0		# No Mode Specified
li      $v0 13		# Open File

syscall
bltz	$v0 main_err	# Negative means open failed

move	$a0 $v0		# point at open file
la      $a1 binary	# write into my binary space
li      $a2 2048	# read a file of at max 2kb
li      $v0 14		# Read File Syscall
syscall
la      $t0 binary
add     $t0 $t0 $v0	# point to end of binary space

li      $t1 0xFFFFFFFF	# place ending sentinel
sw      $t1 0($t0)

# fix all jump instructions
la      $t0 binary	# point at start of instructions
move	$t1 $t0
main_jumpFixLoop:
    lw      $t2 0($t0)
    srl     $t3 $t2 26	# primary opCode
    li      $t4 2       # 2 is the jump opcode
    beq     $t3 $t4 main_jumpFix
    li      $t4 3       # 3 is the jal opcode
    beq     $t3 $t4 main_jumpFix
    j		main_jfIncrem
    main_jumpFix:
    #Replace upper 10 bits of jump with binary address
    li      $t3 0xFC000FFF	# bitmask
    and     $t2 $t2 $t3		# clear bits
    la      $t4 binary
    srl     $t4 $t4 2		# align to instruction
    not     $t3 $t3
    and     $t4 $t4 $t3		# only get bits in field
    or      $t2 $t2 $t4		# combine back on the binary address
    addi    $t2 $t2 -9      # adjust for the first 9 lines
                            # when spim loads a program
    sw      $t2 0($t0)      # place the modified instruction
    main_jfIncrem:
    addi	$t0 $t0 4
    li      $t4 -1
    bne     $t2 $t4 main_jumpFixLoop

la      $a0 binary	#prepare pointers for assignment
jal     findLive
move    $a0 $v0 
jal     writeArray

j       main_done

main_err:
la      $a0 noFileStr
li      $v0 4
syscall
main_done:

li      $v0 10
syscall


#-----------------------------------------------------------
# writeArray writes out the live registers
# that have been gathered in a nice format
#
# input:
# $a0: the array to write out
#-----------------------------------------------------------

writeArray:

addi    $sp $sp -24
sw      $ra 0($sp)
sw      $s0 4($sp)
sw      $s1 8($sp)
sw      $s2 12($sp)
sw      $s3 16($sp)
sw      $s4 20($sp)

move    $s0 $a0
li      $s1 0xFFFFFFFF      # sentinel to look for, for end of array

writeArrayLoop:
    lw      $s2 0($s0)
    beq     $s2 $s1 writeArrayDone  # if array entry == -1 : done
    addi	$s0 $s0 4
    la      $a0 liveMessage     # print the generic live message
                                # for each entry in the array
    li      $v0 4
    syscall

    # Print the contents of the vector lists

    #iterate over each bit and print as needed
    li      $t2, 0                  # shamt = 0
    li      $t3, 32
    vLPbits:                        # while True
        beq     $t2, $t3, vLPbend	# if shamt = 32: break
        srlv	$t4, $s2, $t2       # bit = (word >> shamt) AND 0x1
        andi	$t4, $t4, 0x1
        beq     $t4, $zero, vLPbcont # if bit == 1
        la      $t4, zero
        addi	$t5, $zero, 5
        mult	$t5, $t2
        mflo	$t5
        add     $a0, $t4, $t5
        li      $v0, 4
        syscall
        la      $a0 space
        li      $v0 4
        syscall
        vLPbcont:
        addi	$t2, $t2, 1         # shamt = shamt + 1
        j       vLPbits
    vLPbend:
    la      $a0 format      #newline
    li      $v0 4
    syscall
    j       writeArrayLoop
writeArrayDone:
lw      $ra 0($sp)
lw      $s0 4($sp)
lw      $s1 8($sp)
lw      $s2 12($sp)
lw      $s3 16($sp)
lw      $s4 20($sp)
addi    $sp $sp 24
jr      $ra

#####---------  Student code goes here  ---------#####
