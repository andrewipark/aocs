from functools import cmp_to_key as c2k
from itertools import chain, pairwise
import numpy as np

# ffs
R= '\033[0m'
cols = ['\033[30m', '\033[38;5;8m', '\033[38;140;8m']

def p0(grid):
	for x in grid:
		print(''.join((cols[y] + '█' for y in x)) + R)

def main():
	with open('i14.txt') as f:
		inputs = [x.strip().split(' -> ') for x in f.read().split('\n')]
	inputs.pop() # ending \n
	# flip from x,y to r,c for terminal display
	inputs = [[tuple([int(x) for x in p.split(',')][::-1]) for p in l] for l in inputs]
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

	p0(board)


if __name__ == '__main__':
	main()
