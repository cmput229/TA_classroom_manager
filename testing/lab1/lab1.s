#---------------------------------------------------------------
# Assignment:           <number>
# Due Date:             <date>
# Name:                 <name>
# Unix ID:              <ID>
# Lecture Section:      <section>
# Instructor:           <instructor>
# Lab Section:          <section> <time>
# Teaching Assistant:   <TA>
#---------------------------------------------------------------

#---------------------------------------------------------------
#
#   Comments section:
#       Please add your comments here!
#   Register usage:
#       Please note which registers are used for which purposes here!
#
#---------------------------------------------------------------

.data

.text

main:
	li	$v0, 5				# syscall readint
	syscall					# $v0 <- 0xWWXXYYZZ

	andi $t0, $v0, 0xFF     # $t0 <- 0x000000ZZ
    sll  $a0, $t0, 8        # $a0 <- 0x0000ZZ00 
    srl  $v0, $v0, 8        # $v0 <- 0x00WWXXYY
    andi $t0, $v0, 0xFF     # $t0 <- 0x000000YY
    or   $a0, $a0, $t0      # $v0 <- 0x0000ZZYY
    sll  $a0, $a0, 8        # $a0 <- 0x00ZZYY00
    srl  $v0, $v0, 8        # $v0 <- 0x0000WWXX
    andi $t0, $v0, 0xFF     # $t0 <- 0x000000XX
    or   $a0, $a0, $t0      # $a0 <- 0x00ZZYYXX
    sll  $a0, $a0, 8        # $a0 <- 0xZZYYXX00
    srl  $v0, $v0, 8        # $v0 <- 0x000000WW
    or   $a0, $a0, $v0      # $a0 <- 0xZZYYXXWW

	li	$v0, 1				# syscall printint
	syscall
	jr	$ra					# Return
