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

def part_a(sensors, Y):
	beacons = set(((s[2], s[3]) for s in sensors))
	closed_ranges = []
	for s in sensors:
		sense_dist = abs(s[0] - s[2]) + abs(s[1] - s[3])
		dist_to_y = abs(s[1] - Y)
		sense_range = sense_dist - dist_to_y
		if sense_range < 0:
			continue
		closed_ranges.append((s[0] - sense_range, s[0] + sense_range))

	# brute force
	if True:
		start_x = min((min(s[0], s[2]) for s in sensors)) * 6
		end_x = max((max(s[0], s[2]) for s in sensors)) * 6
		covered = 0
		for i in range(start_x, end_x + 1):
			for rd, rf in closed_ranges:
				if rd <= i <= rf:
					covered += 1
					break

		return covered - len([b for b in beacons if b[1] == Y])

def main():
	with open('i15.txt') as f:
		sensors = sensors_from_input(f.read())
	print(part_a(sensors, 2000000))

if __name__ == '__main__':
	main()
