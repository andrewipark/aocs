from functools import reduce
from operator import and_
from itertools import groupby

def rucksack(l):
	s = len(l) // 2
	return l[:s], l[s:]

def one_common_item(*i):
	result = reduce(and_, (set(v) for v in i))
	assert len(result) == 1, result # ffs
	return list(result)[0]

def prio(x):
	assert len(x) == 1, x
	if x < 'a':
		return ord(x) - ord('A') + 26 + 1
	else:
		return ord(x) - ord('a') + 1

with open('3.txt') as f:
	print(sum((prio(str(one_common_item(*rucksack(l)))) for l in f)))

with open('3.txt') as f:
	print(
		sum((prio(str(one_common_item(*[i.strip() for _k, i in g])))
			 for _k, g in groupby(enumerate(f), lambda i: i[0] // 3)
		))
	)
