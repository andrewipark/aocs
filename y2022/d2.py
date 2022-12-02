import heapq
from enum import IntEnum, auto

class RPS(IntEnum):
	ROCK = 0
	PAPER = auto()
	SCISSORS = auto()

def which(a: RPS, b: RPS) -> int:
	"""-1, 0, or 1 for a, tie, b"""
	return \
		[[0, -1, 1],
		 [1, 0, -1],
		 [-1, 1, 0]][a][b]
	# there's a better way to do this but I'm too lazy

def p(l):
	a, b = (ord(x) for x in l.split())
	return (RPS(a - ord('A')), RPS(b - ord('X')))

with open('2.txt') as f:
	print([p(x) for x in f][:5])
