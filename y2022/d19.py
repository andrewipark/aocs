import operator as op
import re
from functools import cache
from multiprocessing import Pool as mpool

# resource tuples: (ore, clay, obsidian, geode)

MAX_RESOURCES = 4
GEODE = 3

def afford(have, cost):
	assert len(have) == len(cost)
	return all(map(op.ge, have, cost))

def bill(have, cost):
	assert len(have) == len(cost)
	return tuple(map(op.sub, have, cost))

def give(have, what):
	assert len(have) == len(what)
	return tuple(map(op.add, have, what))

def zeros_except_one(l, i):
	a = [0] * l
	a[i] = 1
	return a

def l(text):
	s = []
	for i, l in enumerate(text.strip().split('\n')):
		m = re.fullmatch(
			r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'
		, l)
		assert m, l
		assert int(m[1]) - 1 == i
		vals = list(map(lambda i: int(m[i + 2]), range(6)))

		s.append((
			(vals[0], 0, 0, 0),
			(vals[1], 0, 0, 0),
			(vals[2], vals[3], 0, 0),
			(vals[4], 0, vals[5], 0),
		))
	return s

def max_geodes(t, costs):
	builders = (1, 0, 0, 0)
	resources = (0, 0, 0, 0)
	max_ore_cost = tuple((max(v) for v in zip(*costs)))
	print(max_ore_cost)

	# SLOW
	@cache
	def score(t, builders, resources):
		if t <= 1:
			#print(t, builders, resources)
			return builders[GEODE] + resources[GEODE]

		# always correct because builders don't become ready until the next turn
		resources_after = give(resources, builders)
		results = [
			score(
				t - 1,
				give(builders, zeros_except_one(MAX_RESOURCES, resource)),
				bill(resources_after, costs[resource])
			)
			for resource in range(MAX_RESOURCES)
			if afford(resources, costs[resource])
			and (resource == GEODE or builders[resource] < 5) # wrong way to make this run more quickly
		]
		# always try to build the next available choice
		if not results or not (
			(builders[1] == 0 and afford(resources, costs[1]))
			or (builders[2] == 0 and afford(resources, costs[2]))
			or (builders[GEODE] == 0 and afford(resources, costs[GEODE]))
		):
			results.append(score(t - 1, builders, resources_after))
		return max(results)

	return score(t, builders, resources)

def part_a_fn(b):
	t = 8 # 24
	return max_geodes(24, b)

def main():
	with open('i19s.txt') as f:
		b = l(f.read())

	with mpool() as p:
		result = list(p.map(part_a_fn, b))
		print(result)
		print(sum(((i + 1 * v) for i, v in enumerate(result))))

if __name__ == '__main__':
	main()
