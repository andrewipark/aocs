from enum import Enum as E, IntEnum as IE, auto
from math import gcd as gdc
from itertools import chain, product

class Turn(E):
	IZQUIERDA = auto()
	ELDERECHO = auto()

# TODO like 9.py
class DRC(IE):
	COLPOS = 0
	ROWPOS = auto()
	COLNEG = auto()
	ROWNEG = auto()

	def t(self, t: Turn):
		if t == Turn.IZQUIERDA:
			v = -1
		elif t == Turn.ELDERECHO:
			v = 1
		cls = type(self)
		return cls((self + v) % len(cls))

	def m(self):
		match self:
			case DRC.ROWPOS: return (1, 0)
			case DRC.COLPOS: return (0, 1)
			case DRC.ROWNEG: return (-1, 0)
			case DRC.COLNEG: return (0, -1)

def process_board(board, flat):
	board_lines = board.split('\n')
	rows, cols = len(board_lines), max((len(l) for l in board_lines))
	cell_size = gdc(rows, cols)
	# sort points into proper category
	walls = set()
	spaces = dict()
	probes = {x: list() for x in DRC}
	start_c = None
	for p in product(range(rows), range(cols)):
		r, c = p
		if c >= len(board_lines[r]):
			continue
		match board_lines[r][c]:
			case '#': walls.add(p)
			case '.': spaces[p] = {}
		if r == 0 and not start_c and (walls or spaces):
			start_c = c
	# figure out adjacency
	# SUBOPTIMAL this could be faster if we coalesced spaces across dimensions
	# and then could "jump" across them instead of traversing them
	for p, d in product(spaces.keys(), DRC):
		next_p = p
		nd = d
		while True:
			next_p = tuple((l + q) % j for l, q, j in zip(next_p, nd.m(), (rows, cols)))
			if next_p in spaces:
				result = next_p
				break
			if next_p in walls:
				result = None
				break
		spaces[p][d] = (result, nd)

	return spaces, start_c

def process_moves(m):
	# I am tired of writing regex or parsing code
	moves_l = [[m, Turn.IZQUIERDA] for m in m.split('L')]
	moves_l[-1].pop()
	m2 = list(chain.from_iterable(moves_l))
	moves_r = [list(chain.from_iterable((n, Turn.ELDERECHO) for n in m.split('R'))) if isinstance(m, str) else (m,) for m in m2]
	[m.pop() for m in moves_r if isinstance(m, list)]
	return [(int(x) if isinstance(x, str) else x) for x in chain.from_iterable(moves_r)]

def process(board, moves, flat):
	return process_board(board, flat), process_moves(moves)

def do(spaces, pos, d, dist):
	for i in range(dist):
		try:
			next_pos, next_dir = spaces[pos][d]
		except KeyError:
			print(pos, d, pos in spaces, (d in spaces[pos]) if (pos in spaces) else False)
			raise
		if next_pos is None:
			return pos, d, i
		pos, d = next_pos, next_dir
	return pos, d, dist

def part_a(spaces, c, moves):
	pos = (0, c)
	assert pos in spaces
	d = DRC.COLPOS
	for m in moves:
		if isinstance(m, int):
			pos, d, _ = do(spaces, pos, d, m)
		else:
			d = d.t(m) # lmao
		assert pos in spaces
	return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + (d % len(DRC))

def main():
	with open('i22.txt') as f:
		rb, rm = f.read().split('\n\n')

	# part A
	(spaces, c), moves = process(rb, rm, True)
	print(part_a(spaces, c, moves))

if __name__ == '__main__':
	main()
