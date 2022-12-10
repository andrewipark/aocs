def simul(l):
	x = 1
	xs = 0
	cycles = 1 # b/c we want values _during_ a given cycle not after
	# 1-based indexing can die in a fire
	li = 0

	while li < len(l):
		curr = l[li]
		curr_cycles = None
		if curr == 'noop':
			curr_cycles = 1
		else:
			curr_cycles = 2

		for i in range(curr_cycles):
			if (cycles - 20) % 40 == 0:
				xs += (x * cycles)
			cycles += 1

		if curr != 'noop':
			x += int(curr.split(' ')[1])

		li += 1

	return xs

if __name__ == '__main__':
	l = []
	with open('i10.txt') as f:
		l = f.read().split('\n')
	l.pop()

	print(simul(l))
