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

def move(d, l, poses, state):
	for _ in range(l):
		poses[0] = a(poses[0], d)
		# pairwise doesn't work well here
		for l in range(len(poses) - 1):
			pos_h, pos_t = poses[l:l+2]
			delta = pf(lambda i, j: abs(i-j), pos_h, pos_t)
			if max(delta) > 2:
				assert False, (i, pos_h, pos_t, delta)
			if max(delta) == 2:
				# move_t = pf(lambda i, j: s(i-j), pos_h, pos_t)
				# pos_t = pf(operator.add, pos_t, move)
				pos_t = pf(lambda h, t: s(h-t) + t, pos_h, pos_t)

			poses[l:l+2] = [pos_h, pos_t]
		state[poses[-1]] = True

if __name__ == '__main__':
	l = []
	with open('i9.txt') as f:
		l = f.read().split('\n')
	l.pop()
	l = [m.split(' ', 1) for m in l]
	l = [(Dir.o(m[0]), int(m[1])) for m in l]

	for i in (2, 10):
		state = {}
		poses = [(0, 0)] * i
		for m in l:
			move(*m, poses, state)
		print(len(state))
