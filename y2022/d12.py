from collections import deque

def make_grid(abcdf):
	l = [[c for c in x.strip()] for x in abcdf.split()]
	for i, r in enumerate(l):
		for j, x in enumerate(r):
			if x == 'S':
				start = (i, j)
				x = 'a'
			elif x == 'E':
				end = (i, j)
				x = 'z'
			l[i][j] = (ord(x) - ord('a'), None)
	return l, start, end

def cc_height(x):
	assert 0 <= x <= 25
	if x == 25:
		y = 214
	elif x == 24:
		y = 226
	elif x == 23:
		y = 229
	else:
		y = 233 + x
	return f'\033[38;5;{y}m'

R= '\033[0m'

def v0(grid):
	for x in grid:
		print(''.join((cc_height(y[0]) + '█' for y in x)) + R)

def neighbors(grid, pos, visited, val, pred):
	l = []
	if pos[0] > 0:
		l.append(((pos[0] - 1, pos[1]), pos, val))
	if pos[0] < len(grid) - 1:
		l.append(((pos[0] + 1, pos[1]), pos, val))
	if pos[1] > 0:
		l.append(((pos[0], pos[1] - 1), pos, val))
	if pos[1] < len(grid[0]) - 1:
		l.append(((pos[0], pos[1] + 1), pos, val))
	result = [v for v in l if v[0] not in visited and pred(grid, pos, v[0])]
	for v in result:
		visited.add(v[0])
	return result

def p1_pred(grid, src, dst):
	sh = grid[src[0]][src[1]][0]
	dh = grid[dst[0]][dst[1]][0]
	return dh - sh <= 1

def bfs_p1(grid, starts):
	visited = set()
	q = deque([(x, None, 0) for x in starts])
	for s in q:
		visited.add(s[0])
	while q:
		curr, prev, dist = q.popleft()
		grid[curr[0]][curr[1]] = (grid[curr[0]][curr[1]][0], dist)
		q.extend(neighbors(grid, curr, visited, dist + 1, p1_pred))

def locs_where(grid, pred):
	l = []
	for i, r in enumerate(grid):
		for j, x in enumerate(r):
			if pred(x):
				l.append((i, j))
	return l

def reset_grid(grid):
	return [[(x[0], None) for x in y] for y in grid]

def main():
	with open('i12.txt') as f:
		grid, start, end = make_grid(f.read())
	# v0(grid)
	bfs_p1(grid, [start])
	print(grid[end[0]][end[1]])
	grid = reset_grid(grid)
	bfs_p1(grid, locs_where(grid, lambda cell: cell[0] == 0))
	print(grid[end[0]][end[1]])


if __name__ == '__main__':
	main()
