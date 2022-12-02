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

def other_which(opponent: RPS, you_result: int) -> RPS:
	raw = opponent + you_result % 3 # b/c enum values ascend in the cycle of winning
	if raw < 0:
		raw += 3
	raw %= 3
	return RPS(raw)

def p(l):
	a, b = (ord(x) for x in l.split())
	return (RPS(a - ord('A')), RPS(b - ord('X')))

def pb(l):
	a, b = (ord(x) for x in l.split())
	 # now it's the sign of the result we need
	return (RPS(a - ord('A')), b - ord('Y'))

def score(a: RPS, b: RPS):
	return (
		int(b) + 1 # shape score
		+ (which(a, b) + 1) * 3 # outcome score
	)

def scoreb(opponent: RPS, you_result: int):
	shape = other_which(opponent, you_result)
	assert which(opponent, shape) == you_result, (opponent, you_result, shape)
	# print this for me, you dolt
	return (
		shape + 1 # shape score
		+ (you_result + 1) * 3 # outcome score
	)

with open('2.txt') as f:
	print(sum((score(*p(x)) for x in f)))

with open('2.txt') as f:
	print(sum((scoreb(*pb(x)) for x in f)))
