# ok, balanced base 5 is actually sort of cute

SNAFU_TO_INT = {'0': 0, '1': 1, '2': 2, '-': -1, '=': -2}
INT_TO_SNAFU = {v: k for k, v in SNAFU_TO_INT.items()}
BASE = len(SNAFU_TO_INT)
# if we were dealing with long snafu numbers, we'd want a precomputed powers table?

def snafu_to_int(x):
	v = 0
	for i, c in enumerate(x[::-1]):
		v += SNAFU_TO_INT[c] * (5 ** i)
	return v

def int_to_base(i, b):
	assert i >= 0
	if i == 0:
		return [0]
	d = []
	p = b
	while i > 0:
		i, r = divmod(i, p)
		d.append(r)
	return d[::-1]

def int_to_snafu(i):
	v = int_to_base(i, BASE)
	v[0:0] = [0]
	for i in range(len(v) - 1, 0, -1):
		if v[i] > 2:
			v[i-1] += 1
			v[i] -= BASE
	if v[0] == 0:
		del v[0]
	return ''.join((INT_TO_SNAFU[d] for d in v))

def main():
	with open('i25.txt') as f:
		snafus = f.read().strip().split('\n')
		ints = [snafu_to_int(l) for l in snafus]
	resnafus = [int_to_snafu(i) for i in ints]
	assert resnafus == snafus

	print(int_to_snafu(sum(ints)))

if __name__ == '__main__':
	main()
