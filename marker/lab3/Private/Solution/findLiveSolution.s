#-------------------------------
# Lab_findLive solution
# Author: Kristen Newbury
# Date: June 9 2017
#-------------------------------
.data
.align 2
liveRegs:       #the word to store the live regs gathered for one point of interest/after jal trace
    .word 0
knownToBeDead:  #stack to contain the registers found to be dead
    .space 100
visited:        #100 bytes per function, use to indicate which instrs have been visited in a trace
    .space 1100
allLives:       #array of live registers found in program, each entry corresponding to lives at one jal point
    .space 40
.text
#-------------------------
#findLive: for all jal's calls pathTrace, resets globals between each and accumulates results
#into an array of entries corresponding to each jal trace point
#
# register usage:
#   $s0: pointer into program
#   $s1: sentinel for program
#   $s2: literal for opcode check
#   $s3: instr
#   $s4: instr opcode
#   $s5: intermediate result handling
#   $s6: result array pointer
#   $s7: mask for returning only $t and $s regs
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

    move    $s0 $a0     #copy program pointer for safety
    move    $a1 $s0             # $a1  <- start address for the program
    li      $s1 -1      #sentinel for program
    la      $s6 allLives        #result array pointer
    li      $s7 0x03FFFF00      #mask for $s's and $t's
    move    $a2 $zero           #initialize pointer into knownToBeDead for pathTrace fxn call

mainProcessLoop:
#finds jal instr's in program, if jal:do trace, else:continue
    lw      $s3 0($s0)
    beq     $s3 $s1 mainProcessDone     #check for sentinel
    addi	$s0 $s0 4           # increment instruction stream pointer
    srl     $s4 $s3 26          # extract opcode in lower five bits
    li      $s2 3               # $s2 <- Opcode of jal shifted right
    beq     $s2 $s4 callpathTrace  # if it is a jal instruction: trace path

    j       mainProcessLoop

callpathTrace:

    move    $a0 $s0             # $a0  <- address after jal instr / provide as arg to initial pathTrace call
    jal     pathTrace

    lw      $s5 liveRegs
    and     $s5 $s5 $s7         #extract just the $s and $t regs from conservative result
    sw      $s5 0($s6)          #place this in the final array
    addi    $s6 $s6 4

    la      $s5 liveRegs             #clear liveRegs between each function
    sw      $zero 0($s5)
    la      $s5 knownToBeDead        #clear knownToBeDead's first entry between each function
    sw      $zero 0($s5)

    j       mainProcessLoop

mainProcessDone:

    sw      $s1 0($s6)      #terminate results vector with a -1
    la      $v0 allLives    #return pointer to result array

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
#pathTrace: find the live registers for one instruction by calling gatherRegs
#decides which instr to process next based on if this instruction was a branch, jump or other
#processing of the 'next' is dealt with by a recursive call to self
#
# register usage:
#   $s0: pointer into program
#   $s1: sentinel for program
#   $s2: instr opcode
#   $s3: imm for $ra reg val check, then opcode checks
#   $s4: PC+4
#   $s5: imm for bit setting of visited
#
#
# input:
#   $a0: the address to start this portion of the path trace from
#   $a1: the beginning address of the program
#   $a2: current index into knownToBeDead
#--------------------------
pathTrace:
    addi    $sp $sp -28
    sw      $ra 0($sp)
    sw      $s0 4($sp)
    sw      $s1 8($sp)
    sw      $s2 12($sp)
    sw      $s3 16($sp)
    sw      $s4 20($sp)
    sw      $s5 24($sp)

    move    $a3 $a0         #just safe keeping in case we wanted to print
    addi    $s4 $a3 4       #PC = PC + 4 , for next instruction to check on

    #check if this instr has been visited before
    sub     $s0 $a3 $a1     #index= address-beginningAddress
    la      $s1 visited
    add     $s1 $s1 $s0     #$s1 <- index into visited
    lbu     $s0 0($s1)      #s0  <- visited[index]
    bne     $s0 $zero liveDone      #if visited[index] != 0: trace of this path is done

    lw      $s0 0($a3)      #$s0 <- fetch instruction
    srl     $s2 $s0 26      #extract opcode

    bne     $s2 $zero skipJrCheck   #if opcode != 0: do not bother checking if it jr $ra
    sll     $s5 $s0 6       #extract bits 25-21 for register check
    srl     $s5 $s5 27
    li      $s3 31          #to check for $ra
    beq     $s5 $s3 liveDone        #if instruction == jr $ra: trace of this path is done

skipJrCheck:
    li      $s5 1
    sb      $s5 0($s1)       #visited[index] = 1 : set the visited indicator for this instruction in this path

    move    $a0 $s0
    jal     gatherRegs      #parse the instruction for reg vals

    li      $s3 2            #j instr opcode
    bne     $s3 $s2 notJump  #if instr!= jump: check if it is branch

    #if instruction == jump: calculate the target address
    sll     $s3 $s0 6
    srl     $s3 $s3 4       #instruction 26 lowermost sll 2
    srl     $s5 $s4 28      #pc+4 uppermost 4 bits
    sll     $s5 $s5 28
    or      $a0 $s5 $s3
    jal     pathTrace          #pathTrace(jump target)
    j       liveDone

notJump:
    #check opcodes for branch instr
    li      $s3 1   #bgez/bltz
    beq     $s3 $s2 branch
    li      $s3 4   #beq
    beq     $s3 $s2 branch
    li      $s3 5   #bne
    beq     $s3 $s2 branch
    li      $s3 6   #blez
    beq     $s3 $s2 branch
    li      $s3 7   #bgtz
    beq     $s3 $s2 branch

elseCondition:
    #else: pathTrace(PC+4)
    move    $a0 $s4
    jal     pathTrace
    j       liveDone

branch:
    #if instruction == branch:
    la      $s3 knownToBeDead
    add     $s3 $s3 $a2
    lw      $s5 0($s3)      #get current knownToBeDead entry
    sw      $s5 4($s3)      #save it in the next position to use as copy for subsequent call
    addi    $a2 $a2 4       #index into knownToBeDead ++
    #calculate the branch target
    sll     $s3 $s0 16
    sra     $s3 $s3 14      #instruction 16 lowermost sll 2 and sign extended
    add     $a0 $s4 $s3     #pc+4 + offset = branch target address
    jal     pathTrace          #pathTrace(branch target)

    addi    $a2 $a2 -4      #index into knownToBeDead --

    j       elseCondition   #branches must traverse both pathes

liveDone:

    sb      $zero 0($s1)       #visited[index] = 0 : reset the visited indicator

    lw      $ra 0($sp)
    lw      $s0 4($sp)
    lw      $s1 8($sp)
    lw      $s2 12($sp)
    lw      $s3 16($sp)
    lw      $s4 20($sp)
    lw      $s5 24($sp)
    addi    $sp $sp 28
    jr      $ra
#-------------------------
#gatherRegs: parses an instruction and sets some bits in
#the gathered live result as well as the knownToBeDead array
# rearranges the regs of the instr so that Itype/Rtype can be handled by same code
#
# register usage:
#   $s0: knownToBeDead stack pointer then knownToBeDead stack entry value
#   $s1: $rd
#   $s2: $rs
#   $s3: $rt
#   $s4: instr opcode and then entry from liveRegs
#   $s5: literal for opcode to check against
#   $s6: literal for setting bits in liveRegs/knownToBeDead
#   $s7: liveRegs word address
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

    la      $s7 liveRegs
    la      $s0 knownToBeDead
    add     $s0 $s0 $a2     #current knownToBeDead index
    lw      $s1 0($s0)
    move    $s0 $s1         # $s0 <- current knownToBeDead entry

    #will treat $s1 as only dst and $s2 and $s3 as only source, rearrange so that it is true and kill non regs
    sll     $s1 $a0 6
    srl     $s2 $s1 27      #$s2 <- rs
    sll     $s1 $s1 5
    srl     $s3 $s1 27      #$s3 <- rt
    sll     $s1 $s1 5
    srl     $s1 $s1 27      #$s1 <- rd

    srl     $s4 $a0 26      #opcode

    #check for some odd branches, save instructions and ignores jumps
    li      $s5 1       #bgez/btlz
    beq     $s5 $s4 oddBranch
    li      $s5 2       #j
    beq     $s5 $s4 gatherDone
    li      $s5 3       #jal
    beq     $s5 $s4 gatherDone
    li      $s5 4       #beq
    beq     $s5 $s4 normalBranch
    li      $s5 5       #bne
    beq     $s5 $s4 normalBranch
    li      $s5 6       #blez
    beq     $s5 $s4 oddBranch
    li      $s5 7       #bgtz
    beq     $s5 $s4 oddBranch
    li      $s5 0x2b    #sw
    beq     $s5 $s4 normalBranch
    li      $s5 0x28    #sb
    beq     $s5 $s4 normalBranch
    li      $s5 0x29     #sh
    beq     $s5 $s4 normalBranch

    beq     $s4 $zero processRegs   #if (instr != any of above types) & (opcode == 0): instr == R-type

    #else: rearrange regs bc in I type $rt is dst
    move    $s1 $s3     #$s1 <- rt : $s1 contains the one true destination register for both types of instr
    move    $s3 $zero   #$s3 <- 0

processRegs:
#possibly set two regs as found live
    li      $s6 1           #for setting bits
    #set bits in the liveness vector first
    sllv    $s5 $s6 $s2
    and     $s4 $s5 $s0     #get bit in knownToBeDead to do a check
    bne     $s4 $zero noRs  #if this reg is known to be dead: skip this reg
    #else: set as live
    lw      $s4 0($s7)      #store rs val
    or      $s4 $s4 $s5
    sw      $s4 0($s7)

noRs:
    sllv    $s5 $s6 $s3
    and     $s4 $s5 $s0     #get bit in knownToBeDead to do a check
    bne     $s4 $zero setKnownDead  #if this reg is known to be dead: skip this reg
    #else: set as live
    lw      $s4 0($s7)      #store rt val
    or      $s4 $s4 $s5
    sw      $s4 0($s7)
    j       setKnownDead

oddBranch:
    #rd and rt are non valid values in bgez/bltz/blez/bgtz
    move    $s1 $zero       #kill nonvalid registers
    move    $s3 $zero
    j       processRegs

normalBranch:
    #rd is non valid value in beq/bne/sw/sh/sb
    move    $s1 $zero       #kill nonvalid registers
    j       processRegs

setKnownDead:
    #set bits in knownToBeDead vector
    sllv    $s5 $s6 $s1
    or      $s5 $s5 $s0     #or the set bit with current knownToBeDead entry
    la      $s1 knownToBeDead
    add     $s1 $s1 $a2     #current knownToBeDead index
    sw      $s5 0($s1)      #store destination reg val

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
