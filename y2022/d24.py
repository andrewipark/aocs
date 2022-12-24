from collections import defaultdict as ddd, deque
from itertools import product
import operator as op
from math import prod

# still more grid drudgery

def process(board_lines):
	rows, cols = len(board_lines) - 2, max((len(l) for l in board_lines)) - 2
	# sort points into proper category
	storms_rows = ddd(list)
	storms_cols = ddd(list)
	for p in product(range(rows), range(cols)):
		r, c = p
		match board_lines[r+1][c+1]:
			case '<': storms_rows[r].append((c, -1))
			case '>': storms_rows[r].append((c, 1))
			case '^': storms_cols[c].append((r, -1))
			case 'v': storms_cols[c].append((r, 1))
	return storms_rows, storms_cols, rows, cols

# much of this copied from 12 with minor alterations
def neighbors(dims, storms, pos, visited, val):
	l = [(pos, pos, val)]
	if pos[0] > 0 or (pos == (0, 0)):
		l.append(((pos[0] - 1, pos[1]), pos, val))
	if pos[0] < dims[0] - 1 or (pos[0] == dims[0] - 1 and pos[1] == dims[1] - 1):
		l.append(((pos[0] + 1, pos[1]), pos, val))
	if pos[1] > 0 and 0 <= pos[0] < dims[0]:
		l.append(((pos[0], pos[1] - 1), pos, val))
	if pos[1] < dims[1] - 1 and 0 <= pos[0] < dims[0]:
		l.append(((pos[0], pos[1] + 1), pos, val))
	result = [v for v in l if (v[0], val) not in visited and storms_pred(dims, storms, v[0], val)]
	for v in result:
		visited.add((v[0], val))
	return result

def storms_pred(dims, storms, pos, val):
	for s in storms[0][pos[0]]:
		if (s[0] + val * s[1]) % dims[1] == pos[1]:
			return False
	for s in storms[1][pos[1]]:
		if (s[0] + val * s[1]) % dims[0] == pos[0]:
			return False
	return True

def bfs_p1(dims, storms, start, time, goal):
	visited = set()
	q = deque([((start, None, time))])
	for s in q:
		visited.add((s[0], s[2]))
	while q:
		curr, prev, dist = q.popleft()
		if curr == goal:
			return dist
		q.extend(neighbors(dims, storms, curr, visited, dist + 1))

def main():
	with open('i24.txt') as f:
		r = process(f.read().strip().split('\n'))
	dims = r[2:4]
	storms = r[0:2]

	wauerignflsrhygbisrekgse = (-1, 0)
	wevtwsgdfjghsoerijhprttr = (dims[0], dims[1] - 1)

	# part a
	t = bfs_p1(dims, storms, wauerignflsrhygbisrekgse, 0, wevtwsgdfjghsoerijhprttr)
	print(t)

if __name__ == '__main__':
	main()
