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

	# Flip the integer here!

	li	$v0, 1				# syscall printint
	syscall
	jr	$ra					# Return
