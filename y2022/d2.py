from enum import IntEnum, auto

# why are all these numbers 1-indexed??

class RPS(IntEnum):
	ROCK = 0
	PAPER = auto()
	SCISSORS = auto()

	def score(self) -> int:
		return int(self) + 1

def result(opponent: RPS, you: RPS) -> int:
	"""-1, 0, or 1 for opponent, tie, you"""
	return \
		[[0, -1, 1],
		 [1, 0, -1],
		 [-1, 1, 0]][you][opponent]
	# there's a better way to do this but I'm too lazy to handle wraparound

def which(opponent: RPS, you_result: int) -> RPS:
	raw = opponent + you_result % 3 # b/c enum values ascend in the cycle of winning
	if raw < 0:
		raw += 3
	raw %= 3
	return RPS(raw)

def pa(l):
	a, b = (ord(x) for x in l.split())
	return (RPS(a - ord('A')), RPS(b - ord('X')))

def pb(l):
	a, b = (ord(x) for x in l.split())
	# now it's the sign of the result we need
	return (RPS(a - ord('A')), b - ord('Y'))

def score(opponent: RPS, you: RPS):
	return (
		you.score()
		+ (result(opponent, you) + 1) * 3 # outcome score
	)

def scoreb(opponent: RPS, you_result: int):
	shape = which(opponent, you_result)
	assert result(opponent, shape) == you_result, (opponent, you_result, shape)

	return (
		shape.score()
		+ (you_result + 1) * 3 # outcome score
	)
	# or: score(opponent, shape)

def main():
	with open('2.txt') as f:
		print(sum((score(*pa(x)) for x in f)))
	with open('2.txt') as f:
		print(sum((scoreb(*pb(x)) for x in f)))

if __name__ == '__main__':
	main()
