from operator import add

def process(txt):
	return [tuple(map(int, e.split(','))) for e in txt.split()]

def process_a(data):
	cube_locs = dict() # location -> open adjacent

	for loc in data:
		assert loc not in cube_locs
		cube_locs[loc] = 6
		for d in range(3):
			for j in (-1, 1):
				loc_delta = [0, 0, 0]
				loc_delta[d] += j
				loc_adjacent = tuple(map(lambda p: add(*p), zip(loc, loc_delta)))
				if loc_adjacent in cube_locs:
					cube_locs[loc_adjacent] -= 1
					cube_locs[loc] -= 1
				# if loc_adjacent comes later, then loc will be handled in this loop

	return cube_locs, sum(cube_locs.values())

def main():
	with open('i18.txt') as f:
		cubes = process(f.read().strip())
	raw, area = process_a(cubes)
	print(area)
	print(raw)

if __name__ == '__main__':
	main()
