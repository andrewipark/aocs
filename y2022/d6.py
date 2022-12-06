from collections import deque

def first_run_of_n_unique(iterable, n):
	# bounded dequeues don't return what was pushed off the end :(
	q = deque()
	# it'd be better to use a multiset here, but n is small so no one cares
	for i, c in enumerate(iterable):
		q.append(c)
		if len(q) > n:
			q.popleft()
		if len(set(q)) == n:
			return i

	return None

v: str = None
with open('i6.txt') as f:
	v = f.read().strip()

def solve(iterable, n):
	result = first_run_of_n_unique(v, n)
	assert result
	# it returns the 0-based index of the character
	what = v[result-n+1:result+1]
	assert len(set(what)) == n
	print(result + 1, what)

solve(v, 4)
solve(v, 14)
