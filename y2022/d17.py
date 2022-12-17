import re
from functools import cache
from itertools import product
from math import gcd
import numpy as np

def simul(dirs, n, cheat):
	rocks = [
		['####'],
		[
			'.#.',
			'###',
			'.#.',
		],
		[
			# flip this from the problem text because y (I guess r) is height
			'###',
			'..#',
			'..#'
		],
		['#'] * 4,
		['##'] * 2,
	]

	rocks_nd = []
	for rock in rocks:
		nd = np.zeros((len(rock), len(rock[0])), dtype=np.int8)
		for i, j in product(range(len(rock)), range(len(rock[0]))):
			nd[i,j] = 1 if rock[i][j] == '#' else 0
		rocks_nd.append(nd)

	curr_height = 0
	calc_height = 0
	dir_counter = 0
	well = np.zeros((100, 7))

	def ws(rock, rock_r, rock_c):
		return well[
			rock_r : rock_r + rock.shape[0],
			rock_c : rock_c + rock.shape[1]
		]

	d = dict() # (dir_index, rock_index) -> states
	last_deltas = [] # see loop below

	i = 0
	while i < n:
		rock = rocks_nd[i % len(rocks_nd)]
		rock_r = curr_height + 3
		rock_c = 2

		# check for {direction, rock} indices we've already simulated before
		# I thought we'd have to do a height map, but apparently not
		st = (dir_counter % len(dirs), i % len(rocks_nd))
		if st in d and cheat:
			d[st].append((i, curr_height))
			if len(d[st]) >= 2:
				# compute {rock counter, height} deltas
				x = (d[st][-1][0] - d[st][-2][0], d[st][-1][1] - d[st][-2][1])
				# I am still unsure that this is mathematically sound
				if len(last_deltas) < 1000:
					last_deltas.append(x)
				elif all((v == x for v in last_deltas)):
					# we seem to have stabilized; cheat
					cycles = max((n - i - 1) // x[0], 0)
					calc_height += x[1] * cycles
					i += x[0] * cycles
					print(cycles, x, st, i)
				else:
					last_deltas.clear()
		else:
			d[st] = [(i, curr_height)]

		while True:
			shift = dirs[dir_counter % len(dirs)]
			dir_counter += 1

			# fugly horizontal shift calculations
			shift_ok = True
			if (rock_c == 0 and shift == -1) or (rock_c + rock.shape[1] >= 7 and shift == 1):
				shift_ok = False # well

			if shift_ok:
				well_dest = ws(rock, rock_r, rock_c + shift)
				if np.any(np.logical_and(well_dest, rock)):
					shift_ok = False # some other rock

			if shift_ok:
				rock_c += shift

			# vertical shift (aka gravity)
			shift_ok = True
			if rock_r == 0 or np.any(np.logical_and(ws(rock, rock_r - 1, rock_c), rock)):
				well[
					rock_r : rock_r + rock.shape[0],
					rock_c : rock_c + rock.shape[1]
				] = np.logical_or(ws(rock, rock_r, rock_c), rock)
				break
			rock_r -= 1

		curr_height = max(curr_height, rock_r + rock.shape[0])
		if curr_height + 8 >= well.shape[0]:
			well.resize((well.shape[0] * 4 // 3, well.shape[1]), refcheck = False)
		i += 1

	return curr_height + calc_height

def main():
	with open('i17.txt') as f:
		dirs = [-1 if c == '<' else 1 for c in f.read().strip()]
	print(simul(dirs, 2022, False))
	assert simul(dirs, 10000, False) == simul(dirs, 10000, True)
	print(simul(dirs, 1000000000000, True))

if __name__ == '__main__':
	main()
