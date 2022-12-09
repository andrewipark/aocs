from enum import Enum as E
import operator

class Dir(E):
	DOWN = (0, -1)
	LEFT = (-1, 0)
	RIGHT = (1, 0)
	UP = (0, 1)

	@staticmethod
	def o(s):
		n = {'R': 'RIGHT', 'D': 'DOWN', 'L': 'LEFT', 'U': 'UP'}
		return Dir[n[s]]

def pf(f, pos_a, pos_b):
	return tuple((f(i, j) for i, j in zip(pos_a, pos_b)))

def a(pos, d):
	return pf(operator.add, pos, d.value)

def s(x):
	if x > 0:
		return 1
	if x < 0:
		return -1
	return 0

def move(d, l, pos_h, pos_t, state):
	for _ in range(l):
		pos_h = a(pos_h, d)
		delta = pf(lambda i, j: abs(i-j), pos_h, pos_t)
		if max(delta) > 2:
			assert False, (pos_h, pos_t, delta)
		if max(delta) == 2:
			# move_t = pf(lambda i, j: s(i-j), pos_h, pos_t)
			# pos_t = pf(operator.add, pos_t, move)
			pos_t = pf(lambda h, t: s(h-t) + t, pos_h, pos_t)
		state[pos_t] = True

	return pos_h, pos_t

if __name__ == '__main__':
	l = []
	with open('i9.txt') as f:
		l = f.read().split('\n')
	l.pop()
	l = [m.split(' ', 1) for m in l]
	l = [(Dir.o(m[0]), int(m[1])) for m in l]

	state = {}
	pos_h = (0, 0)
	pos_t = (0, 0)
	for m in l:
		pos_h, pos_t = move(*m, pos_h, pos_t, state)

	print(len(state))
