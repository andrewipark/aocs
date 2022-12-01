import heapq
heap = [[-1, None]] * 3
with open('1.txt') as f:
	current = [0, 0]
	for line in f:
		line = line.strip()
		if not line:
			heapq.heappushpop(heap, current[:])
			current[1] += 1
			current[0] = 0
		else:
			current[0] += int(line)
print(heap)
print(sum(x[0] for x in heap))
