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
		s.append(tuple(map(int, (m[1], m[2], m[3], m[4]))))
	return s

def coalesce_closed_ranges(x):
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
	return [n for n in new if n]

def data(sensors, Y, constrain = False):
	beacons = set(((s[2], s[3]) for s in sensors))
	closed_ranges = []
	for s in sensors:
		sense_dist = abs(s[0] - s[2]) + abs(s[1] - s[3])
		dist_to_y = abs(s[1] - Y)
		sense_range = sense_dist - dist_to_y
		if sense_range < 0:
			continue
		closed_ranges.append((s[0] - sense_range, s[0] + sense_range))

	return beacons, coalesce_closed_ranges(closed_ranges)

def part_a(sensors, beacons, closed_ranges, Y):
	# brute force
	if False:
		start_x = min((min(s[0], s[2]) for s in sensors)) * 6
		end_x = max((max(s[0], s[2]) for s in sensors)) * 6
		covered = 0
		for i in range(start_x, end_x + 1):
			for rd, rf in closed_ranges:
				if rd <= i <= rf:
					covered += 1
					break

		return covered - len([b for b in beacons if b[1] == Y])

	return sum((f - d + 1 for d, f in closed_ranges)) - len([b for b in beacons if b[1] == Y])

def main():
	with open('i15.txt') as f:
		sensors = sensors_from_input(f.read())
	Y = 2000000
	print(part_a(sensors, *data(sensors, Y), Y))

if __name__ == '__main__':
	main()
