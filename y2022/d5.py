import re

with open('5.txt') as f:
	initial_lines, moves_lines = [x.split('\n') for x in f.read().split('\n\n')]
	initial_lines.pop() # don't emit sequential numbers like this, damn it
	guess_crates = len(initial_lines[0])
	guess_crates //= 4
	guess_crates += 1 # because falta ending '\n'
	moves_lines.pop() # there's an ending '\n'?

	state = [[] for x in range(guess_crates)]
	for l in initial_lines:
		for x in range(guess_crates):
			idx = 4 * x + 1
			s = l[idx:idx+1].strip()
			if s:
				state[x].append(s)

	# so that stuff at the "top" vertically goes to the end
	state = [x[::-1] for x in state]

	moves = [] # (num, from, to)
	for l in moves_lines:
		m = re.fullmatch(r'move (\d+) from (\d+) to (\d+)', l)
		assert m, l
		num, src, dst = (int(x) for x in m.group(1,2,3))
		moves.append((num, src-1, dst-1))

	for num, src, dst in moves:
		assert len(state[src]) >= num
		# yes you can do slicing but idc
		for i in range(num):
			state[dst].append(state[src].pop())

	print(''.join((x[-1] for x in state)))
