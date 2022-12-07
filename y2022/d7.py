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

def print_dir(e, m: dict[tuple[str], Any], curr_path: list[str] = None):
	if isinstance(e, File):
		print('    ' *  len(curr_path), e)
	elif isinstance(e, Dir):
		print('    ' * len(curr_path), e.name + ": " + str(m.get(curr_path)))
		if e.entries is None:
			print('    ' * (len(curr_path) + 1), '!!!!! UNVISITED !!!!!')
	else:
		raise ValueError()

def visit(d: Dir, f, curr_path: list[str] = None):
	if curr_path is None:
		curr_path = tuple()
	f(d, curr_path)
	for e in d.entries.values():
		if isinstance(e, File):
			f(e, curr_path)
		elif isinstance(e, Dir):
			new_path = tuple(list(curr_path) + [e.name])
			visit(e, f, new_path)
		else:
			raise ValueError

def print_dir_cb(m: dict[tuple[str], Any]):
	def print_dir_closure(e, curr_path: list[str] = None):
		print_dir(e, m, curr_path)
	return print_dir_closure

if __name__ == '__main__':
	with open('i7.txt') as f:
		commands = [x.strip().split('\n') for x in f.read().split('$ ')]
	commands = [(c[0], c[1:]) for c in commands[2:]]
	print(commands[:5])

	tree = parse(commands)
	visit(tree, print_dir_cb({}))
