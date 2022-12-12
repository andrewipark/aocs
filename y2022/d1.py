import heapq

# I like Cal's (g.split() for g in text_blob.split("\n\n")) better
def split_it(i):
	lines = []
	for line in i:
		line = line.strip()
		if not line:
			yield lines
			lines = []
		else:
			lines.append(line)

def main():
	with open('1.txt') as f:
		# pt1: use max
		print(heapq.nlargest(3, (sum(int(b) for b in a) for a in split_it(f))))

if __name__ == '__main__':
	main()
