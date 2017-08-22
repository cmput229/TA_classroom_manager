#-------------------------------
# Lab- isLive
#
# Author: Kristen Newbury
# Date: June 9 2017
#-------------------------------

.data

.align 2
liveRegs:
    .word 0
knownToBeDead:
    .space 100
knownEnd:
    .word -1
visited:        #currently 100 bytes for a max 100 line function
    .space 100
allLives:
    .space 40
.text

#-------------------------
#findLive
#
# for all jal's call's isLive
#
# input:
#   $a0: address of program to process
# output:
#   $v0: address of list of registers that are live at each function call
#--------------------------
findLive:

addi    $sp $sp -36
sw      $ra 0($sp)
sw      $s0 4($sp)
sw      $s1 8($sp)
sw      $s2 12($sp)
sw      $s3 16($sp)
sw      $s4 20($sp)
sw      $s5 24($sp)
sw      $s6 28($sp)
sw      $s7 32($sp)

move    $a1 $a0
move    $s0 $a0
li      $s1 -1
li      $t1 -2
la      $s6 allLives
li      $s7 0x03FFFF00      #mask for $s's and $t's

move    $a2 $zero

mainProcessLoop:

lw      $s3 0($s0)

beq     $s3 $s1 mainProcessDone     #check for sentinel
addi	$s0 $s0 4           #increment instruction stream pointer
srl     $s4 $s3 26          #extract opcode
li      $s2 3
beq     $s2 $s4 callIsLive

j       mainProcessLoop

callIsLive:

move    $a0 $s0
jal     isLive
jal     clearKnownToBeDead


la      $s5 liveRegs
lw      $s5 0($s5)
and     $s5 $s5 $s7       #extract just the $s and $t regs from conservative result
sw      $s5 0($s6)
addi    $s6 $s6 4

la      $s5 liveRegs        #clear liveRegs between each function
sw      $zero 0($s5)

j       mainProcessLoop

mainProcessDone:

li      $s0 -1      #terminate results vector with a -1
sw      $s0 0($s6)

la      $v0 allLives

lw      $ra 0($sp)
lw      $s0 4($sp)
lw      $s1 8($sp)
lw      $s2 12($sp)
lw      $s3 16($sp)
lw      $s4 20($sp)
lw      $s5 24($sp)
lw      $s6 28($sp)
lw      $s7 32($sp)
addi    $sp $sp 36
jr  $ra


#-------------------------
#isLive
#
#
# input:
#   $a0: the address to start from
#   $a1: the beginning address of the program
#   $a2: current index into knownToBeDead
#--------------------------
isLive:
addi    $sp $sp -36
sw      $ra 0($sp)
sw      $s0 4($sp)
sw      $s1 8($sp)
sw      $s2 12($sp)
sw      $s3 16($sp)
sw      $s4 20($sp)
sw      $s5 24($sp)
sw      $s6 28($sp)
sw      $s7 32($sp)

move    $a3 $a0     #just safe keeping in case we wanted to print

sub     $s0 $a3 $a1     #index= address-beginningAddress
addi    $s4 $a3 4


la      $s1 visited
add     $s1 $s1 $s0     #$s1 <- index
move    $s0 $zero       #clear this just in case lb wont, only a problem in qtspim apparently
lb      $s0 0($s1)      #s0 <- visited[index]
bne     $s0 $zero liveDone

lw      $s0 0($a3)      #$s0 <- instruction
srl     $s2 $s0 26      #extract opcode

bne     $s2 $zero skipJrCheck
sll     $s5 $s0 6       #extract bits 25-21
srl     $s5 $s5 27
li      $s3 31
beq     $s5 $s3 liveDone        #instruction == jr $ra

skipJrCheck:
li      $s5 1
sb      $s5 0($s1)       #visited[index] = 1

move    $a0 $s0
jal     gatherRegs

li      $s3 2
bne     $s3 $s2 notJump

#if instruction == jump:
sll     $s3 $s0 6
srl     $s3 $s3 4       #instruction 26 lowermost sll 2
srl     $s5 $s4 28      #pc+4 uppermost 4
sll     $s5 $s5 28
or      $a0 $s5 $s3
jal     isLive          #isLive(target)
j       liveDone

notJump:

li      $s3 1
beq     $s3 $s2 branch
li      $s3 4
beq     $s3 $s2 branch
li      $s3 5
beq     $s3 $s2 branch
li      $s3 6
beq     $s3 $s2 branch
li      $s3 7
beq     $s3 $s2 branch

elseCondition:
#else: isLive(address+4)
move    $a0 $s4
jal     isLive
j       liveDone

branch:
#if instruction == branch:
la      $s3 knownToBeDead
add     $s3 $s3 $a2
lw      $s5 0($s3)      #get current knownToBeDead entry
sw      $s5 4($s3)      #save it in the next position to use as copy for subsequent call
addi    $a2 $a2 4       #index into knownToBeDead ++

sll     $s3 $s0 16
sra     $s3 $s3 14      #instruction 16 lowermost sll 2 and sign extended
add     $a0 $s4 $s3     #pc+4 + offset
move    $s7, $a2
jal     isLive          #isLive(target)
move    $a2, $s7

addi    $a2 $a2 0      #index into knownToBeDead --

j       elseCondition   #branches must traverse both pathes

liveDone:

move    $s0 $zero
sb      $s0 0($s1)       #visited[index] = 0

lw      $ra 0($sp)
lw      $s0 4($sp)
lw      $s1 8($sp)
lw      $s2 12($sp)
lw      $s3 16($sp)
lw      $s4 20($sp)
lw      $s5 24($sp)
lw      $s6 28($sp)
lw      $s7 32($sp)
addi    $sp $sp 36
jr      $ra

#-------------------------
#gatherRegs
#
#
# input:
#   $a0: the instruction to parse
#   $a2: current index into knownToBeDead
#--------------------------
gatherRegs:

addi    $sp $sp -36
sw      $ra 0($sp)
sw      $s0 4($sp)
sw      $s1 8($sp)
sw      $s2 12($sp)
sw      $s3 16($sp)
sw      $s4 20($sp)
sw      $s5 24($sp)
sw      $s6 28($sp)
sw      $s7 32($sp)

move    $s1 $zero
la      $s7 liveRegs
la      $s0 knownToBeDead
add     $s0 $s0 $a2     #current knownToBeDead index
lw      $s1 0($s0)
move    $s0 $zero
move    $s0 $s1         # $s0 <- current knownToBeDead entry

#will treat $s1 as only dst and $s2 and $s3 as only source, rearrange so that it is true and kill non regs
sll     $s1 $a0 6
srl     $s2 $s1 27      #$s2 <- rs
sll     $s1 $s1 5
srl     $s3 $s1 27      #$s3 <- rt
sll     $s1 $s1 5
srl     $s1 $s1 27      #$s1 <- rd

srl     $s4 $a0 26

#check for some odd branches and eliminate jumps
li      $s5 1
beq     $s5 $s4 oddBranch
li      $s5 2
beq     $s5 $s4 gatherDone
li      $s5 3
beq     $s5 $s4 gatherDone
li      $s5 4
beq     $s5 $s4 normalBranch
li      $s5 5
beq     $s5 $s4 normalBranch
li      $s5 6
beq     $s5 $s4 oddBranch
li      $s5 7
beq     $s5 $s4 oddBranch
li      $s5 43              #for sw
beq     $s5 $s4 normalBranch

beq     $s4 $zero processRegs

#rearrange regs bc in I type $rt is dst
move    $s1 $s3     #$s1 <- rt
move    $s3 $zero   #$s3 <- 0

processRegs:

li      $s6 1       #for setting bits

#set bits in the liveness vector first
sllv    $s5 $s6 $s2
and     $s4 $s5 $s0     #get bit in knownToBeDead to do a check
bne     $s4 $zero noRs

lw      $s4 0($s7)      #store rs val
or      $s4 $s4 $s5
sw      $s4 0($s7)

noRs:
sllv    $s5 $s6 $s3     #get bit in knownToBeDead to do a check
and     $s4 $s5 $s0
bne     $s4 $zero noRt

lw      $s4 0($s7)      #store rt val
or      $s4 $s4 $s5
sw      $s4 0($s7)

noRt:
j       setKnownDead

oddBranch:
move    $s1 $zero       #kill non registers
move    $s3 $zero
j       processRegs

normalBranch:
move    $s1 $zero       #kill non registers
j       processRegs

setKnownDead:

#set bits in knownToBeDead vector
sllv    $s5 $s6 $s1
or      $s5 $s5 $s0    #or the set bit with current knownToBeDead entry
la      $s1 knownToBeDead
add     $s1 $s1 $a2     #current knownToBeDead index
sw      $s5 0($s1)

gatherDone:

lw      $ra 0($sp)
lw      $s0 4($sp)
lw      $s1 8($sp)
lw      $s2 12($sp)
lw      $s3 16($sp)
lw      $s4 20($sp)
lw      $s5 24($sp)
lw      $s6 28($sp)
lw      $s7 32($sp)
addi    $sp $sp 36
jr  $ra

#----------------------------------------------------------------------------
# clearKnownToBeDead clears the array for each jal since we are using globals
#
#
#----------------------------------------------------------------------------
clearKnownToBeDead:

addi    $sp $sp -24
sw      $ra 0($sp)
sw      $s0 4($sp)
sw      $s1 8($sp)
sw      $s2 12($sp)
sw      $s3 16($sp)
sw      $s4 20($sp)

li      $s0 -1
la      $s2 knownToBeDead
move    $s3 $zero


clearLoop:
lw      $s1 0($s2)
beq     $s1 $s0 clearDone
sw      $s3 0($s2)
addi    $s2 $s2 4
j       clearLoop

clearDone:

move    $a2 $zero       #zero the global index

lw      $ra 0($sp)
lw      $s0 4($sp)
lw      $s1 8($sp)
lw      $s2 12($sp)
lw      $s3 16($sp)
lw      $s4 20($sp)
addi    $sp $sp 24

jr      $ra

