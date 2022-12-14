import re

# omfg
def sign(x):
	if x > 0:
		return 1
	if x < 0:
		return -1
	return 0

def sensors_from_input(text):
	s = []
	for l in text.strip().split('\n'):
		m = re.fullmatch(
			r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)'
		, l)
		assert m, l
		s.append(tuple((int(m[x]) for x in range(1, 4+1))))
	return s

def coalesce_closed_ranges(x, constrain = None):
	subsumed = [False for _ in x]
	new = []

	# fix containing ranges
	for i, r in enumerate(x):
		if subsumed[i]:
			continue
		for j, s in enumerate(x[i+1:], i+1):
			rd, rf = r
			sd, sf = s
			if rd <= sd and sf <= rf:
				subsumed[j] = True
				continue
			if sd <= rd and rf <= sf:
				subsumed[i] = True
				break
		if not subsumed[i]:
			new.append(r) # survived

	# fix half-overlapping ranges
	new.sort()
	i = 0
	j = 1
	while j < len(new):
		p, n = new[i], new[j]
		if p[1] >= n[0]:
			new[i] = (p[0], n[1])
			new[j] = None
		else:
			i = j
		j += 1

	if constrain:
		return [(max(n[0], constrain[0]), min(n[1], constrain[1])) for n in new if n]
	else:
		return [n for n in new if n]

def data(sensors, Y, constrain = None):
	beacons = set(((s[2], s[3]) for s in sensors))
	closed_ranges = []
	for s in sensors:
		sense_dist = abs(s[0] - s[2]) + abs(s[1] - s[3])
		dist_to_y = abs(s[1] - Y)
		sense_range = sense_dist - dist_to_y
		if sense_range < 0:
			continue
		closed_ranges.append((s[0] - sense_range, s[0] + sense_range))

	closed_ranges = coalesce_closed_ranges(closed_ranges, constrain)
	return beacons, closed_ranges

def part_a(sensors, beacons, closed_ranges, Y):
	return sum((f - d + 1 for d, f in closed_ranges)) - len([b for b in beacons if b[1] == Y])

def part_b(guesses, sensors, height):
	for i in guesses:
		beacons, closed_ranges = data(sensors, i, (0, height))
		# ignore beacons because they're already covered
		if (part_a(sensors, [], closed_ranges, i) != height + 1):
			print(i, closed_ranges)
			assert len(closed_ranges) == 2
			j = closed_ranges[0][1] + 1
			return j * height + i
	return None

def main():
	with open('i15.txt') as f:
		sensors = sensors_from_input(f.read())
	Y = 2000000
	print(part_a(sensors, *data(sensors, Y), Y))
	print(part_b((2767556,), sensors, 2 * Y))
	# SUBOPTIMAL range(Y * 2 + 1))) takes about 50 seconds
	# internal corporate discussion: prune based on the positions of the beacons?
	# and then test the edges? not sure how that one works

if __name__ == '__main__':
	main()
