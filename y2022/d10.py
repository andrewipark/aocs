def simul(l):
	x = 1
	xs = 0
	cycles = 1 # b/c we want values _during_ a given cycle not after
	# 1-based indexing can die in a fire
	li = 0
	crt = [[False] * 40 for i in range(6)]

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
			c = cycles - 1
			crt[c // 40][c % 40] = (abs(x - (c % 40)) <= 1)
			cycles += 1

		if curr != 'noop':
			x += int(curr.split(' ')[1])
			print(x)

		li += 1

	return xs, crt

# TODO
A = '\033[30m'
B= '\033[90m'
R= '\033[0m'

if __name__ == '__main__':
	l = []
	with open('i10.txt') as f:
		l = f.read().split('\n')
	l.pop()

	xs, crt = simul(l)
	print(xs)
	for x in crt:
		# TODO how do we detect whether we need 1 char (most ASCII fonts) or 2 char?
		print(''.join(((B if y else A) + '██' + R for y in x)))
