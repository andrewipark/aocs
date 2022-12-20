def mix(s):
	i = 0
	processed = []
	processed_expected = [c[0] for c in s]
	while i < len(s):
		curr = s[i]
		v = curr[0]
		assert curr[1] == 0
		assert v == processed_expected[len(processed)], (i, v, processed_expected[len(processed)])
		processed.append(v)

		del s[i]
		dest = (i + v) % len(s)
		if (dest == 0 and v < 0):
			dest = len(s) # wtf
		# print(i, v, dest)
		s[dest:dest] = [[v, curr[1] + 1]]
		# print([c[0] for c in s])

		if dest <= i:
			i += 1
		while i < len(s) and s[i][1] > 0:
			i += 1
	assert processed == processed_expected, (processed, processed_expected)
	assert all((lambda c: c[0] == 1 for c in s))

def main():
	with open('i20.txt') as f:
		b = [[int(x), 0] for x in f.read().strip().split('\n')]

	# A
	mix(b)
	# print([c[0] for c in b])
	zi = b.index([0, 1])
	print(b[(zi + 1000) % len(b)][0] + b[(zi + 2000) % len(b)][0] + b[(zi + 3000) % len(b)][0])

if __name__ == '__main__':
	main()
