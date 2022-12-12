import re

def move_a(d, s, l):
	for i in range(l):
		d.append(s.pop())

def move_b(d, s, l):
	d.extend(s[-l:])
	del s[-l:]

def do(state, moves, mf):
	for num, src, dst in moves:
		assert len(state[src]) >= num
		mf(state[dst], state[src], num)

def main():
	with open('5.txt') as f:
		initial_lines, moves_lines = [x.split('\n') for x in f.read().split('\n\n')]
	initial_lines.pop() # rm numbering
	# x crates generates a line of len x * 4 - 1
	guess_crates = len(initial_lines[0]) // 4 + 1
	moves_lines.pop() # rm last blank line b/c file is well behaved

	state = [[] for x in range(guess_crates)]
	for l in initial_lines:
		for x in range(guess_crates):
			idx = 4 * x + 1
			s = l[idx:idx+1].strip()
			if s:
				state[x].append(s)

	# so that stuff at the "top" vertically goes to the end
	state_a = [x[::-1] for x in state]
	state_b = [x[:] for x in state_a]

	moves = [] # (num, from, to)
	for l in moves_lines:
		m = re.fullmatch(r'move (\d+) from (\d+) to (\d+)', l)
		assert m, l
		num, src, dst = (int(x) for x in m.group(1,2,3))
		moves.append((num, src-1, dst-1))

	do(state_a, moves, move_a)
	do(state_b, moves, move_b)

	print(''.join((x[-1] for x in state_a)))
	print(''.join((x[-1] for x in state_b)))

if __name__ == '__main__':
	main()
