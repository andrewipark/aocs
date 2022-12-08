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

with open('8.txt') as f:
	data = [[[int(v), False] for v in x] for x in f.read().strip().split('\n')]

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
