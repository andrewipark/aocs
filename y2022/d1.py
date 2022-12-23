import heapq

def main():
	with open('1.txt') as f:
		# pt1: use max
		print(heapq.nlargest(3, (sum(int(b) for b in a) for a in (g.split() for g in f.read().split('\n\n')))))

if __name__ == '__main__':
	main()
