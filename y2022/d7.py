from collections import namedtuple as nt
from typing import Any

commands = []

root_dir = {}

# It's probably redundant to store the name in the entry classes AND the entry map keys.

File = nt('File', ('name', 'size')) # str, int

class Dir:
	def __init__(self, n):
		self.name = n
		self.entries = None # map[str, Union[File, Dir]]

	def __repr__(self):
		return "Dir(" + str(self.name) + " -> " + str(self.entries) + ")"

def parse_ls_output(x: list[str]):
	e = dict()
	for r, n in (l.split(' ', 1) for l in x):
		if r == "dir":
			e[n] = Dir(n)
		else:
			e[n] = File(n, int(r))
	return e

def dir_stack_str(s):
	return '/'.join((d.name for d in dir_stack))

def parse(commands) -> Dir:
	dir_stack: List[Dir] = [Dir('')]

	for command, output in commands:
		wd = dir_stack[-1]
		if command == 'ls':
			if wd.entries:
				print('!! overwriting !!', dir_stack_str(dir_stack))
			wd.entries = parse_ls_output(output)
		elif command.startswith('cd'):
			dest = command.split(' ', 1)[1]
			if dest == '..':
				dir_stack.pop()
				continue
			if dest not in wd.entries:
				print('entry ', dest, ' not in ', wd)
			if not isinstance(wd.entries[dest], Dir):
				print('entry ', dest, ' not a file: ', wd)
			dir_stack.append(wd.entries[dest])
		else:
			print('unhandled', command, output)

	return dir_stack[0]

def print_dir(e, m: dict[tuple[str], Any], curr_path: tuple[str] = None):
	if isinstance(e, File):
		print('    ' *  len(curr_path), e)
	elif isinstance(e, Dir):
		print('    ' * len(curr_path), e.name + ": " + str(m.get(curr_path)))
		if e.entries is None:
			print('    ' * (len(curr_path) + 1), '!!!!! UNVISITED !!!!!')
	else:
		raise ValueError

def calc_size(e, m: dict[tuple[str], Any], curr_path: tuple[str] = None):
	if isinstance(e, File):
		m[tuple(list(curr_path) + [e.name])] = e.size
	elif isinstance(e, Dir):
		size = sum((m[tuple(list(curr_path) + [f])] for f in e.entries.keys()))
		m[tuple(list(curr_path))] = size
	else:
		raise ValueError

def clear_file_keys(e, m: dict[tuple[str], Any], curr_path: tuple[str] = None):
	if isinstance(e, File):
		del m[tuple(list(curr_path) + [e.name])]

def visit(d: Dir, f, curr_path: tuple[str] = None, post: bool = False):
	if curr_path is None:
		curr_path = tuple()
	if not post:
		f(d, curr_path)
	for e in d.entries.values():
		if isinstance(e, File):
			f(e, curr_path)
		elif isinstance(e, Dir):
			new_path = tuple(list(curr_path) + [e.name])
			visit(e, f, new_path, post)
		else:
			raise ValueError
	if post:
		f(d, curr_path)

def visit_cb(m: dict[tuple[str], Any], f):
	def visit_closure(e, curr_path: tuple[str] = None):
		f(e, m, curr_path)
	return visit_closure

if __name__ == '__main__':
	with open('i7.txt') as f:
		commands = [x.strip().split('\n') for x in f.read().split('$ ')]
	commands = [(c[0], c[1:]) for c in commands[2:]]

	tree = parse(commands)
	m = {}
	visit(tree, visit_cb(m, calc_size), post = True)
	# visit(tree, visit_cb(m, print_dir))
	# otherwise we'll double count file sizes
	visit(tree, visit_cb(m, clear_file_keys))
	# part 1
	print(sum((v for v in m.values() if v <= 100000)))

	# part 2
	used = m[tuple()]
	total = 70_000000
	free = total - used
	need = 30_000000
	delta = need - free
	print(used, total, free, need, delta)
	print(min((v for v in m.values() if v >= delta)))
