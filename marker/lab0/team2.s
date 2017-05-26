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
	li   $v0, 5				# syscall readint
	syscall					# $v0 <- 0xWWXXYYZZ

    addi $t0, $0, 0xFF      # $t0 <- 0x000000FF
    and  $a0, $t0, $v0      # $a0 <- 0x000000ZZ
    sll  $a0, $a0, 24       # $a0 <- 0xZZ000000
    sll  $t0, $t0, 8        # $t0 <- 0x0000FF00
    and  $t1, $t0, $v0      # $t1 <- 0x0000YY00
    sll  $t1, $t1, 8        # $t1 <- 0x00YY0000
    or   $a0, $a0, $t1      # $a0 <- 0xZZYY0000
    sll  $t0, $t0, 8        # $t0 <- 0x00FF0000
    and  $t1, $t1, $v0      # $t1 <- 0x00XX0000
    srl  $t1, $t1, 8        # $t1 <- 0x0000XX00
    or   $a0, $a0, $t1      # $a0 <- 0xZZYYXX00
    sll  $t0, $t0, 8        # $t0 <- 0xFF000000
    and  $t1, $v0, $t0      # $t1 <- 0xWW000000
    srl  $t1, $t1, 24       # $t1 <- 0x000000WW
    or   $a0, $a0, $t1      # $a0 <- 0xZZYYXXWW

	li	$v0, 1				# syscall printint
	syscall
	jr	$ra					# Return
