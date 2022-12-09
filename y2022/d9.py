from enum import Enum as E

class Dir(E):
	DOWN = (0, -1)
	LEFT = (-1, 0)
	RIGHT = (1, 0)
	UP = (0, 1)

	@staticmethod
	def o(s):
		n = {'R': 'RIGHT', 'D': 'DOWN', 'L': 'LEFT', 'U': 'UP'}
		return Dir[n[s]]

if __name__ == '__main__':
	l = []
	with open('i9.txt') as f:
		l = f.read().split('\n')
	l.pop()
	l = [m.split(' ', 1) for m in l]
	l = [(Dir.o(m[0]), int(m[1])) for m in l]
	print(l)
