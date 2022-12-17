import re
from functools import cache
from itertools import product
import numpy as np

def simul(dirs, n):
	rocks = [
		['####'],
		[
			'.#.',
			'###',
			'.#.',
		],
		[
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
	dir_counter = 0
	well = np.zeros((100, 7))

	def ws(rock, rock_r, rock_c):
		return well[
			rock_r : rock_r + rock.shape[0],
			rock_c : rock_c + rock.shape[1]
		]

	for i in range(n):
		rock = rocks_nd[i % len(rocks_nd)]
		rock_r = curr_height + 3
		rock_c = 2

		while True:
			shift = dirs[dir_counter % len(dirs)]
			dir_counter += 1

			# fugly shift calculations
			shift_ok = True
			if (rock_c == 0 and shift == -1) or (rock_c + rock.shape[1] >= 7 and shift == 1):
				shift_ok = False # well

			if shift_ok:
				well_dest = ws(rock, rock_r, rock_c + shift)
				if np.any(np.logical_and(well_dest, rock)):
					shift_ok = False # some other rock

			if shift_ok:
				rock_c += shift

			# vertical clearance
			shift_ok = True
			if rock_r == 0 or np.any(np.logical_and(ws(rock, rock_r - 1, rock_c), rock)):
				# can't use ws for some reason
				well[
					rock_r : rock_r + rock.shape[0],
					rock_c : rock_c + rock.shape[1]
				] = np.logical_or(ws(rock, rock_r, rock_c), rock)
				break
			rock_r -= 1

		curr_height = max(curr_height, rock_r + rock.shape[0])
		if curr_height + 8 >= well.shape[0]:
			well.resize((well.shape[0] * 4 // 3, well.shape[1]), refcheck = False)

	return curr_height

def main():
	with open('i17.txt') as f:
		dirs = [-1 if c == '<' else 1 for c in f.read().strip()]
	print(simul(dirs, 2022))

if __name__ == '__main__':
	main()
