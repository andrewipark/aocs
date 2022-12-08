def trace(grid, start: tuple[int, int], d: tuple[int, int]):
	c0, c1 = start
	d0, d1 = d
	height = None
	while c0 >= 0 and c0 < len(grid) and c1 >= 0 and c1 < len(grid):
		cell = grid[c0][c1]
		if height is None or height < cell[0]:
			cell[1] = True
			height = cell[0]
		c0 += d0
		c1 += d1

A = '\033[31m'
B= '\033[32m'
R= '\033[0m'

def distance_to_edge(c0, c1, d0, d1, g):
	result = 0
	if d0 == 1:
		result += c0
	if d0 == -1:
		result += (g - 1 - c0)
	if d1 == 1:
		result += c1
	if d1 == -1:
		result += (g - 1 - c1)
	return result

def distance_between(c0a, c0b, c1a, c1b):
	cad = abs(c0a - c1a)
	cbd = abs(c0b - c1b)
	assert cad == 0 or cbd == 0
	return cad + cbd

def why(grid, start: tuple[int, int], d: tuple[int, int]):
	c0, c1 = start
	d0, d1 = d
	g = len(grid)
	assert d0 == 0 or d1 == 0 and (d0 + d1) != 0
	heights = {}
	while c0 >= 0 and c0 < len(grid) and c1 >= 0 and c1 < len(grid):
		cell = grid[c0][c1]
		cp = heights.get(cell[0])
		if cp is None:
			cell[2] *= distance_to_edge(c0, c1, d0, d1, g)
		else:
			cell[2] *= distance_between(c0, c1, *cp)
		# what we really want is an ordered map, but with only 10 values, no one cares
		for i in range(0, cell[0] + 1):
			heights[i] = (c0, c1)

		c0 += d0
		c1 += d1

with open('8.txt') as f:
	data = [[[int(v), False, 1] for v in x] for x in f.read().strip().split('\n')]

	g = len(data)

	for i in range(0, g):
		# wasteful to traverse the edges but makes my life easier
		trace(data, (0, i), (1, 0))
		trace(data, (g - 1, i), (-1, 0))
		trace(data, (i, 0), (0, 1))
		trace(data, (i, g - 1), (0, -1))

	for x in data:
		print(''.join(((B if y[1] else A) + str(y[0]) + R for y in x)))

	print(sum((sum((1 for y in x if y[1])) for x in data)))

	for i in range(0, g):
		why(data, (0, i), (1, 0))
		why(data, (g - 1, i), (-1, 0))
		why(data, (i, 0), (0, 1))
		why(data, (i, g - 1), (0, -1))

	print(max((max((y[2] for y in x)) for x in data)))
