from functools import cmp_to_key as c2k
from itertools import chain, pairwise
import numpy as np

# ffs
R= '\033[0m'
cols = ['\033[30m', '\033[38;5;8m', '\033[38;5;22m']

def p0(grid):
	for x in grid:
		print(''.join((cols[y] + '█' for y in x)) + R)

def simul_grain(board, la, lb):
	while True:
		while la < board.shape[0] and board[la, lb] == 0:
			la += 1
		if la >= board.shape[0]:
			return None # fell off the bottom
		if board[la, lb] != 0:
			if lb <= 0:
				return None # fell off left
			if board[la, lb - 1] == 0:
				lb -= 1
				continue
			if lb >= board.shape[1]:
				return None # fell off right
			if board[la, lb + 1] == 0:
				lb += 1
				continue
			# all three spots are occupied
			la -= 1
			return la, lb
		raise ValueError

def input_from_text(text):
	inputs = [x.split(' -> ') for x in text.strip().split('\n')]
	# flip from x,y to r,c for terminal display
	return [[tuple([int(x) for x in p.split(',')][::-1]) for p in l] for l in inputs]

def grid_from_input(inputs, part2 = False):
	# normalize c
	max_a = max((p[0] for p in chain.from_iterable(inputs)))
	max_b = max((p[1] for p in chain.from_iterable(inputs)))
	min_b = min((p[1] for p in chain.from_iterable(inputs)))
	inputs = [[(a, b - min_b) for a, b in l] for l in inputs]
	board = np.zeros((max_a + 1, max_b - min_b + 1), dtype=np.int8)
	# sand at 0, 500 - min_b

	for l in inputs:
		for m, n in pairwise(l):
			ma, mb = m
			na, nb = n
			assert (ma != na) != (mb != nb)

			if ma != na:
				pa, qa = min(ma, na), max(ma, na)
				board[pa:qa+1, nb] = 1
			else:
				pb, qb = min(mb, nb), max(mb, nb)
				board[ma, pb:qb+1] = 1

	return board, min_b

def part_a(board, min_b):
	c = 0
	while True:
		result = simul_grain(board, 0, 500 - min_b)
		if not result:
			break
		c += 1
		ga, gb = result
		board[ga, gb] = 2
	return c

def main():
	with open('i14.txt') as f:
		inputs = input_from_text(f.read())

	a_board, a_min_b = grid_from_input(inputs)
	a_count = part_a(a_board, a_min_b)
	p0(a_board)
	print(a_count)

if __name__ == '__main__':
	main()
