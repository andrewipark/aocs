import operator as op
import re
from functools import cache
from math import prod
from multiprocessing import Pool as mpool

# resource tuples: (ore, clay, obsidian, geode)

MAX_RESOURCES = 4
GEODE = 3

def afford(have, cost):
	assert len(have) == len(cost)
	return all(map(op.ge, have, cost))

def give(have, what):
	assert len(have) == len(what)
	return tuple(map(op.add, have, what))

def turns_to_make(cost, have, rate):
	if any((c != 0 and r == 0 for c, r in zip(cost, rate))):
		return None
	return max(max(((c - h + r - 1) // r for c, h, r in zip(cost, have, rate) if r != 0)), 0)

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
	max_resource_cost = [max(z) for z in zip(*costs)]
	max_resource_cost[GEODE] = float('inf')

	@cache
	def score(t, builders, resources):
		turns_to_builder = [turns_to_make(costs[resource], resources, builders) for resource in range(MAX_RESOURCES)]

		results = [
			score(
				t - turns_to_builder[resource] - 1,
				give(builders, zeros_except_one(MAX_RESOURCES, resource)),
				tuple((
					cr - c + b * (turns_to_builder[resource] + 1)
					for cr, c, b in zip(resources, costs[resource], builders)
				))
			)
			for resource in range(MAX_RESOURCES)
			if turns_to_builder[resource] is not None
			and t > turns_to_builder[resource] + 1
			# no point in more builders if we'd make more than we can consume
			and builders[resource] < max_resource_cost[resource]
		]
		# SUBOPTIMAL per reddit, a better pruning strategy
		# tracks the top-level maximum geodes so far and stops
		# if the "current" branch cannot possibly beat that maximum
		# other heuristics, e.g. always build a geode robot,
		# might fail on pathological input but seem to be ok for AoC
		if not results:
			# won't be able to build anything else in time
			return t * builders[GEODE] + resources[GEODE]
		return max(results)

	return score(t, builders, resources)

def part_a_fn(b):
	return max_geodes(24, b)

def part_b_fn(b):
	return max_geodes(32, b)

def main():
	with open('i19.txt') as f:
		b = l(f.read())

	with mpool() as p:
		result_a = list(p.map(part_a_fn, b))
		print(result_a)
		print(sum(((i + 1) * v for i, v in enumerate(result_a))))

		# naive multiprocessing doesn't help with this state space or only 3 inputs
		# sharding some of the top level calls might help but seems complicated
		result_b = list(p.map(part_b_fn, b[:3]))
		print(result_b)
		print(prod(result_b))

if __name__ == '__main__':
	main()
