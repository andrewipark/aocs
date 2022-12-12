import re

# I want attrs; this is getting stupidly annoying
class Monkey:
	def __init__(self, items, op_str, test_div_num, true_dest, false_dest):
		self.items = items
		self.op_str = op_str
		self.test_div_num = test_div_num
		self.true_dest = true_dest
		self.false_dest = false_dest

	def __repr__(self):
		return "Monkey(" + repr([self.items, self.op_str, self.test_div_num, self.true_dest, self.false_dest]) + ")"

if __name__ == '__main__':
	with open('i11s.txt') as f:
		inputs = [x.strip() for x in f.read().split('\n\n')]

	monkeys = []
	for _i, l in enumerate(inputs):
		m = re.match(
			r'Monkey (\d)+:\s+'
			r'Starting items: ([\d, ]+)\s+'
			r'Operation: new = (.+)\n\s+'
			r'Test: divisible by (\d+)\s+'
			r'If true: throw to monkey (\d+)\s+'
			r'If false: throw to monkey (\d+)'
		, l)
		assert m, l
		assert _i == int(m.group(1))
		monkeys.append(Monkey(
			[int(x) for x in m.group(2).split(', ')],
			m.group(3),
			int(m.group(4)),
			int(m.group(5)),
			int(m.group(6)),
		))

	print(monkeys)

