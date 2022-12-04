def parse(l: str):
	"""fully closed intervals thonk"""
	return [[int(m) for m in l.split('-')] for l in l.strip().split(',')]

def contains(a, b):
	if a[0] <= b[0] and a[1] >= b[1]:
		return True
	if a[0] >= b[0] and a[1] <= b[1]:
		return True
	return False

def overlaps(a, b):
	if a[0] <= b[0] and a[1] >= b[0]:
		return True
	if a[0] <= b[1] and a[1] >= b[1]:
		return True
	if b[0] <= a[0] and b[1] >= a[0]:
		return True
	if b[0] <= a[1] and b[1] >= a[1]:
		return True
	return False
 
with open('4.txt') as f:
	print([parse(x) for x in list(f)[:5]])

with open('4.txt') as f:
	print(sum((1 for x in f if contains(*parse(x)))))

with open('4.txt') as f:
	print(sum((1 for x in f if overlaps(*parse(x)))))
