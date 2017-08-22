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
        .align 2
live:   .space 200          # int v[50]
        .text

findLive:
    la   $v0, live          # $v0 <- Addr(v)
    add  $t0, $v0, $zero    # $t0 <- v*
    addi $t1, $zero, -1     # $t1 <- -1     (-1 == sentinel)
    addi $t2, $v0, 200      # $t2 <- v[50]
initLive:
    sw   $t1, 0($t0)        # *v <- -1
    addi $t0, $t0, 4        # $t0 <- v*++
    bne  $t0, $t2, initLive # *v == v[-1] ? continue; loop

    

    la   $v0, live
    addi $t0, $0, 356
    sw   $t0, 0($v0)
    jr   $ra
