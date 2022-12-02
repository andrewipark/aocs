import heapq
from enum import IntEnum, auto

class RPS(IntEnum):
	ROCK = 0
	PAPER = auto()
	SCISSORS = auto()

def which(opponent: RPS, you: RPS) -> int:
	"""-1, 0, or 1 for opponent, tie, you"""
	return \
		[[0, -1, 1],
		 [1, 0, -1],
		 [-1, 1, 0]][you][opponent]
	# there's a better way to do this but I'm too lazy

def p(l):
	a, b = (ord(x) for x in l.split())
	return (RPS(a - ord('A')), RPS(b - ord('X')))

def score(a: RPS, b: RPS):
	return (
		int(b) + 1 # shape score
		+ (which(a, b) + 1) * 3 # outcome score
	)

with open('2.txt') as f:
	print(sum((score(*p(x)) for x in f)))
