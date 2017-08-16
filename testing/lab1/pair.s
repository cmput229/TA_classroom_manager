HexLoop:
	add	 $t0, $a0, $t1			# $t0 <- $a0 + $t1 (Address s[i])
	lb	 $t4, 0($t0)			# $t4 <- lb($t0) (s[i])
	addi $t0, $t4, -0x30		# $t0 <- $t4 - 0x30 (0x30 = "0")
	slt	 $t3, $t0, $zero		# $t0 < 0 ? goto invalid
	bne	 $t3, $zero, Invalid	# $t0 < 0 ? goto invalid
	slti $t3, $t0, 0xa			# $t0 < 10 ? goto valid	
	bne	 $t3, $zero, Valid		# $t0 < 10 ? goto valid
								# Not in [0, 9]; Maybe in ["A", "F"]
	or	 $t0, $t4, 0x20			# $t0 <- $t4.upper()
	addi $t0, $t0, -0x57		# $t0 <- $t0 - 0x57 ("a" -> 0xA)
	slti $t3, $t0, 0x10			# $t0 > 0xF ? goto invalid
	beq	 $t3, $zero, Invalid	# $t0 > 0xF ? goto invalid

Valid:
	addi $t1, $t1, 1			# $t1 <- $t1++
	sub	 $t3, $t2, $t1			# 
	sll	 $t3, $t3, 2			# $t3 <- 4*i (each char is 4 bits)
	sllv $t0, $t0, $t3			# $t0 <- $t0 << $t3
	or	 $v0, $v0, $t0			# $v0 <- $v0 OR $t0
	slt	 $t3, $t1, $t2			# i < 8? goto HexLoop
	bne  $t3, $zero, HexLoop	# i < 8? goto HexLoop
	addi $v1, $v1, 0			# $v1 <- 0 (Hex String = valid)
	jr	 $ra					# return
	
Invalid:						# invalid:
	addi $v1, $zero, 1			# $v1 <- 1
	jr	 $ra					# return

