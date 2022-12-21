def mix(s, o):
	assert len(s) == len(o)
	processed = []
	expected = [s[i] for i in o]
	poses_o2n = {x: x for x in o}
	for e in o:
		i = poses_o2n[e]
		v = s[i]
		processed.append(s[i])

		del s[i]
		dest = (i + v) % len(s)
		if (dest == 0 and v < 0):
			dest = len(s) # wtf
		# print(e, i, '->', dest)
		s[dest:dest] = [v]
		# print(s)

		this_o2n = dict()
		if dest < i:
			this_o2n = {j: j + 1 for j in range(dest, i)}
		elif dest > i:
			this_o2n = {j + 1: j for j in range(i, dest)}
		this_o2n[i] = dest

		new_o2n = dict()
		for k, v in poses_o2n.items():
			if v in this_o2n:
				new_o2n[k] = this_o2n[v]
		# print(new_o2n)
		for k, v in new_o2n.items():
			poses_o2n[k] = v
		# print(poses_o2n)

	return poses_o2n

def grove(s):
	zi = s.index(0)
	return s[(zi + 1000) % len(s)] + s[(zi + 2000) % len(s)] + s[(zi + 3000) % len(s)]

def part_a(s):
	mix(s, range(len(s)))
	return grove(s)

def part_b(s):
	s = [811589153 * v for v in s]
	o = range(len(s))
	for i in range(10):
		poses = mix(s, o)
		o = [poses[i] for i in o]
	return grove(s)

def main():
	with open('i20.txt') as f:
		b = list(map(int, f.read().strip().split('\n')))

	# A
	s_a = b[:]
	print(part_a(s_a))

	# B
	print(part_b(b))

if __name__ == '__main__':
	main()
