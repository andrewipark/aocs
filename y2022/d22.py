from enum import Enum as E, IntEnum as IE, auto
from itertools import chain, product

class Turn(E):
	IZQUIERDA = auto()
	ELDERECHO = auto()

# TODO like 9.py
class DRC(IE):
	ROWPOS = 0
	COLPOS = auto()
	ROWNEG = auto()
	COLNEG = auto()

	def t(self, t: Turn):
		if t == Turn.IZQUIERDA:
			v = 1
		elif t == Turn.ELDERECHO:
			v = -1
		cls = type(self)
		return cls((self + 1) % len(cls))

	def m(self):
		match self:
			case DRC.ROWPOS: return (1, 0)
			case DRC.COLPOS: return (0, 1)
			case DRC.ROWNEG: return (-1, 0)
			case DRC.COLNEG: return (0, -1)

def process_board(board):
	board_lines = board.split('\n')
	rows, cols = len(board_lines), len(board_lines[0])
	# sort points into proper category
	walls = set()
	spaces = dict()
	gaps = set()
	probes = {x: list() for x in DRC}
	start_c = None
	for p in product(range(rows), range(cols)):
		r, c = p
		match board_lines[r][c]:
			case ' ': gaps.add(p)
			case '#': walls.add(p)
			case '.': spaces[p] = {}
		if r == 0 and not start_c and (walls or spaces):
			start_c = c
	# figure out adjacency
	# SUBOPTIMAL this could be faster if we coalesced spaces across dimensions
	# and then could "jump" across them instead of traversing them
	for p, d in product(spaces.keys(), DRC):
		next_p = p
		while True:
			next_p = tuple((l + q) % j for l, q, j in zip(next_p, d.m(), (rows, cols)))
			if next_p in spaces:
				result = next_p
				break
			if next_p in walls:
				result = None
				break
		spaces[p][d] = result

	return spaces, start_c

def process_moves(m):
	# I am tired of writing regex or parsing code
	moves_l = [[m, Turn.IZQUIERDA] for m in m.split('L')]
	moves_l[-1].pop()
	m2 = list(chain.from_iterable(moves_l))
	moves_r = [list(chain.from_iterable((n, Turn.ELDERECHO) for n in m.split('R'))) if isinstance(m, str) else (m,) for m in m2]
	[m.pop() for m in moves_r if isinstance(m, list)]
	return list(chain.from_iterable(moves_r))

def process(board, moves):
	return process_board(board), process_moves(moves)

def main():
	with open('i22s.txt') as f:
		(spaces, c), moves = process(*f.read().split('\n\n'))

	print(part_a(spaces, c, moves))

if __name__ == '__main__':
	main()
