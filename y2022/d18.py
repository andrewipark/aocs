from itertools import product
from operator import add

def process(txt):
	return [tuple(map(int, e.split(','))) for e in txt.split()]

def euclidean_neighbors(p):
	for d in range(len(p)):
		for j in (-1, 1):
			delta = [0, 0, 0]
			delta[d] += j
			yield tuple(map(add, p, delta))

def cuboid(lo, hi):
	return product(*(range(l, h + 1) for l, h in zip(lo, hi)))

def process_a(data):
	cube_locs = dict() # location -> open adjacent

	for loc in data:
		assert loc not in cube_locs
		cube_locs[loc] = 6
		for loc_adjacent in euclidean_neighbors(loc):
			if loc_adjacent in cube_locs:
				cube_locs[loc_adjacent] -= 1
				cube_locs[loc] -= 1
			# if loc_adjacent comes later, then loc will be handled in this loop

	return cube_locs, sum(cube_locs.values())

def process_b(cube_locs):
	# assume that the corner is within the exterior
	# -/+1 so that we can traverse around the edges later
	loc_min = tuple((min((l[d] for l in cube_locs)) - 1 for d in range(3)))
	loc_max = tuple((max((l[d] for l in cube_locs)) + 1 for d in range(3)))
	assert loc_min, loc_max not in cube_locs

	# WFS (ok, DFS) the exterior
	exterior = set()
	stack = [loc_min]
	while stack:
		loc = stack.pop()
		exterior.add(loc)
		stack.extend((
			n for n in euclidean_neighbors(loc)
			if n not in exterior
			and n not in cube_locs
			and all((low <= c <= high for low, c, high in zip(loc_min, n, loc_max)))
		))

	# the holes must be everything we didn't reach
	holes = (p for p in cuboid(loc_min, loc_max) if p not in exterior and p not in cube_locs)
	holes = list(holes)

	hole_surface_area = process_a(holes)[1]
	return hole_surface_area

def main():
	with open('i18.txt') as f:
		cubes = process(f.read().strip())
	raw, area = process_a(cubes)
	print(area)
	print(area - process_b(raw))

if __name__ == '__main__':
	main()
