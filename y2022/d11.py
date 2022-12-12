import re
import heapq
from copy import deepcopy
from math import prod

# I want attrs; this is getting stupidly annoying
class Monkey:
	def __init__(self, items, op_str, test_div_num, true_dest, false_dest):
		self.items = items
		self.op_str = op_str
		self.op_fn = compile(op_str, '<string>', 'eval')
		self.test_div_num = test_div_num
		self.true_dest = true_dest
		self.false_dest = false_dest
		self.inspect_count = 0

	def __repr__(self):
		return "Monkey(" + repr([self.items, self.op_str, self.test_div_num, self.true_dest, self.false_dest]) + ")"

	def turn(self, reduce_worry):
		results = [] # (worry, dest)[]
		for old in self.items:
			new = eval(self.op_fn)
			if reduce_worry:
				new //= 3
			results.append((new, self.true_dest if new % self.test_div_num == 0 else self.false_dest))
		self.inspect_count += len(self.items)
		self.items.clear()
		return results

def simul(monkeys, turns, reduce_worry):
	safe_mod = prod((m.test_div_num for m in monkeys))
	for _ in range(turns):
		for m in monkeys:
			result = m.turn(reduce_worry)
			for worry, dest in result:
				monkeys[dest].items.append(worry)
		for m in monkeys:
			m.items = [x % safe_mod for x in m.items]

if __name__ == '__main__':
	with open('i11.txt') as f:
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

	for turns, reduce_worry in [(20, True), (10000, False)]:
		monkes = deepcopy(monkeys)
		simul(monkes, turns, reduce_worry)
		print(prod(heapq.nlargest(2, (m.inspect_count for m in monkes))))
