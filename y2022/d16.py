import re
from functools import cache
from collections import defaultdict as ddd

def l(text):
	s = dict()
	for l in text.strip().split('\n'):
		m = re.fullmatch(
			r'Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? ([\w ,]+)'
		, l)
		assert m, l
		e = ddd(lambda: float('inf'))
		for x in m[3].split(', '):
			e[x] = 1
		s[m[1]] = (int(m[2]), e)
	return s

def contract(g):
	to_remove = set((k for k, v in g.items() if v[0] == 0 and len(v[1]) == 2))
	for x in to_remove:
		a, b = g[x][1].keys()
		g[a][1][b] = min(g[a][1].get(b, float('inf')), g[a][1][x] + g[x][1][b])
		g[b][1][a] = min(g[b][1].get(a, float('inf')), g[b][1][x] + g[x][1][a])
		del g[a][1][x], g[b][1][x], g[x]
		assert g[a][1][b] == g[b][1][a], (g[a], g[b]) # symmetry

def fwap(g):
	for p in g:
		g[p][1][p] = 0
		for q in g:
			for r in g:
				w = g[p][1][r]
				t = g[p][1][q] + g[q][1][r]
				g[p][1][r] = min(w, t)
	for p in g:
		del g[p][1][p]

def explore(g, time, e):
	to = time

	@cache
	def score(time, where, ons, e):
		return max(
			[
				(time - dist - 1) * g[n][0] + score(time - dist - 1, n, ons | {n}, e)
				for n, dist in g[where][1].items() if time > dist and n not in ons
			]
			+ [score(to, 'AA', ons, False) if e else 0]
		)
	return score(time, 'AA', frozenset(), e)

def main():
	with open('i16.txt') as f:
		g = l(f.read())
		contract(g)
		fwap(g)

	print(explore(g, 30, False))
	print(explore(g, 26, True))

if __name__ == '__main__':
	main()
