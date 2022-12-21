import operator as ops

def process(lines):
	result = {}
	for l in lines:
		n, expr = l.split(': ')
		try:
			inputs = int(expr)
			op = None
		except ValueError:
			expr = expr.split(' ')
			inputs = [expr[0], expr[2]]
			match expr[1]:
				case '+': op = ops.add
				case '-': op = ops.sub
				case '*': op = ops.mul
				case '/': op = ops.truediv # I'm surprised this doesn't cause floating point errors
				case _: raise ValueError(l)

		result[n] = (op, inputs)
	return result

def e(d, what):
	if what not in d:
		raise ValueError(list(d.keys()), what)
	match d[what]:
		case None, int:
			return d[what][1]
		case fn, inputs:
			evald_inputs = [e(d, i) for i in inputs]
			return fn(*evald_inputs)

def depends_on(d, expr, what):
	if d[expr][1] is int:
		return False
	if what in d[expr][1]:
		return True
	return any((depends_on(d, expr, i) for i in d[expr][1]))

def main():
	with open('i21.txt') as f:
		d = process(f.read().strip().split('\n'))

	# part A
	print(e(d, 'root'))

	# part B
	# SUBOPTIMAL we could CAS this
	lo = -100000000000000000
	hi = 100000000000000000

	which = 0 if depends_on(d, d['root'][1][0], 'humn') else 1
	target = 1 if which == 0 else 0
	target_val = e(d, d['root'][1][target])
	print(target)

	while lo < hi:
		curr = lo + (hi - lo) // 2
		d['humn'] = (None, curr)
		result = e(d, d['root'][1][which])
		# print(curr, result, target_val)
		if result == target_val:
			print('success')
			break
		# BROKEN HARDCODED
		elif result > target_val:
			lo = curr
		else:
			hi = curr
	print(curr)
	for i in range(-2, 2 + 1):
		d['humn'] = (None, curr + i)
		print([e(d, t) for t in d['root'][1]])

if __name__ == '__main__':
	main()
