import re
from collections import defaultdict as ddd

def l(text):
	s = dict()
	for l in text.strip().split('\n'):
		m = re.fullmatch(
			r'Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? ([\w ,]+)'
		, l)
		assert m, l
		s[m[1]] = (int(m[2]), {x: 1 for x in m[3].split(', ')})
	return s

def contract(g):
	to_remove = set((k for k, v in g.items() if v[0] == 0 and len(v[1]) == 2))
	for x in to_remove:
		a, b = g[x][1].keys()
		g[a][1][b] = min(g[a][1].get(b, float('inf')), g[a][1][x] + g[x][1][b])
		g[b][1][a] = min(g[b][1].get(a, float('inf')), g[b][1][x] + g[x][1][a])
		del g[a][1][x], g[b][1][x], g[x]
		assert g[a][1][b] == g[b][1][a], (g[a], g[b]) # symmetry
	return g

def explore(g):
	state = (30, 'AA', set(), 0)
	stack = [state]
	best_states = ddd(lambda: [-1] * 31)
	best = 0
	count = 0
	while stack:
		count += 1
		time, where, ons, score = stack.pop()
		ma = best_states[(where, frozenset(ons))]
		for j in range(time + 1):
			ma[j] = max(ma[j], score)

		if g[where][0] > 0 and where not in ons and time > 0:
			# turn the valve on
			new_ons = ons.copy()
			new_ons.add(where)
			stack.append((time - 1, where, new_ons, score + (time - 1) * g[where][0]))

		stack.extend((
			((time - dist), n, ons, score)
			for n, dist in g[where][1].items()
			if time > dist and (
				n == 'AA' or max(best_states[(n, frozenset(ons))][:1]) < score
			)
		))

		best = max(best, score)

	print(f'explored {count} states')
	return best

def main():
	with open('i16.txt') as f:
		g = contract(l(f.read()))

	print(g)
	print(len(g))

	print(explore(g))

if __name__ == '__main__':
	main()
