from functools import reduce
from operator import and_
from itertools import groupby

def rucksack(l):
	s = len(l) // 2
	return l[:s], l[s:]

def one_common_item(*i):
	result = reduce(and_, (set(v) for v in i))
	assert len(result) == 1, result # ffs
	return result.pop()

def prio(x):
	assert len(x) == 1, x
	if x < 'a':
		return ord(x) - ord('A') + 26 + 1
	else:
		return ord(x) - ord('a') + 1

def a(lines):
	# strip for trailing '\n' doesn't matter b/c (2n + 1) // 2 = n
	return sum((prio(str(one_common_item(*rucksack(l)))) for l in lines))

def b(lines):
	return \
		sum((prio(str(one_common_item(*[i.strip() for _k, i in g])))
			 for _k, g in groupby(enumerate(lines), lambda i: i[0] // 3)
		))

def main():
	with open('3.txt') as f:
		lines = [l for l in f]
		print(a(lines))
		print(b(lines))

if __name__ == '__main__':
	main()
