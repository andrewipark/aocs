from itertools import product
import operator as op
from math import prod

# more grid drudgery; surely this is avoidable...

def process(board_lines):
	rows, cols = len(board_lines), max((len(l) for l in board_lines))
	# sort points into proper category
	mobs = {}
	for p in product(range(rows), range(cols)):
		r, c = p
		match board_lines[r][c]:
			case '#': mobs[p] = [] # list('NSWE') # I thought pt B was going to be that each elf keeps track of its own order list
	return mobs

def propose(board, curr, order):
	for d in product((-1, 0, 1), (-1, 0, 1)):
		if d == (0, 0):
			continue
		if tuple(map(op.add, curr, d)) in board:
			break
	else:
		return None # If no other Elves are in one of those eight positions, the Elf does not do anything
	for d in order:
		match d:
			case 'N': deltas = [(-1, x) for x in (-1, 0, 1)]
			case 'S': deltas = [(1, x) for x in (-1, 0, 1)]
			case 'E': deltas = [(x, 1) for x in (-1, 0, 1)]
			case 'W': deltas = [(x, -1) for x in (-1, 0, 1)]
		if all((tuple(map(op.add, curr, d)) not in board for d in deltas)):
			match d:
				case 'N': return tuple(map(op.add, (-1, 0), curr))
				case 'S': return tuple(map(op.add, (1, 0), curr))
				case 'E': return tuple(map(op.add, (0, 1), curr))
				case 'W': return tuple(map(op.add, (0, -1), curr))
	return None

def move(mobs, order):
	# phase 1
	curr_to_new = dict()
	new_to_curr = dict()
	collisions = set()

	for curr in list(mobs.keys()):
		new = propose(mobs, curr, order)
		if not new:
			continue
		if new not in new_to_curr:
			curr_to_new[curr] = new
			new_to_curr[new] = curr
		elif new not in collisions:
			del curr_to_new[new_to_curr[new]]
			del new_to_curr[new]
			collisions.add(new) # phase 2

	# ludacris
	for curr, new in curr_to_new.items():
		assert new not in mobs
		mobs[new] = mobs[curr]
		del mobs[curr]

	return bool(curr_to_new)

def part(mobs):
	order = 'NSWE'
	for i in range(10):
		if not move(mobs, order):
			break
		order = order[1:] + order[0]
	else:
		i += 1
	# TODO copied from 18 but d = 2 now
	# part A
	loc_min = tuple((min((l[d] for l in mobs)) for d in range(2)))
	loc_max = tuple((max((l[d] for l in mobs)) for d in range(2)))
	volume = prod(((x - n + 1) for x, n in zip(loc_max, loc_min)))

	# part b
	while move(mobs, order):
		i += 1
		order = order[1:] + order[0]
		loc_min = tuple((min((l[d] for l in mobs)) for d in range(2)))
		loc_max = tuple((max((l[d] for l in mobs)) for d in range(2)))

	return volume - len(mobs), i + 1 # one-based indexing is killing me

def main():
	with open('i23t.txt') as f:
		mobs = process(f.read().strip().split('\n'))

	print(part(mobs))

if __name__ == '__main__':
	main()
