# copy-paste
def s(x):
	if x > 0:
		return 1
	if x < 0:
		return -1
	return 0

def c(a, b):
	if isinstance(a, int) and isinstance(b, list):
		return c([a], b)
	if isinstance(a, list) and isinstance(b, int):
		return c(a, [b])
	if isinstance(a, int) and isinstance(b, int):
		return s(a - b)
	if isinstance(a, list) and isinstance(b, list):
		for m, n in zip(a, b):
			r = c(m, n)
			if r != 0:
				return r
		return s(len(a) - len(b))
	raise ValueError

def main():
	with open('i13.txt') as f:
		inputs = [x.strip().split('\n') for x in f.read().split('\n\n')]
	pairs = [tuple((eval(x) for x in p)) for p in inputs]
	# fucking 1-based indexing!!
	print(sum((i + 1 for i, x in enumerate((c(a, b) for a, b in pairs)) if x <= 0)))

if __name__ == '__main__':
	main()
