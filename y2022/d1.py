most = [0, None]
with open('1.txt') as f:
	current = [0, 0]
	for line in f:
		line = line.strip()
		if not line:
			if most[0] < current[0]:
				most = current[:]  # ffs
			current[1] += 1
			current[0] = 0
		else:
			current[0] += int(line)
print(most)
