import sys
import subprocess
from os import listdir

try:
	from tqdm import tqdm
except ImportError:
	class tqdm:
		def __init__(self, **kwargs):
			pass

		def update(self, *args, **kwargs):
			pass

CREATE_NEW_TESTS = False

def pos(n):
	return n > 0

def neg(n):
	return n < 0

class bool_it:
	def __init__(self, n, dig):
		self.n = n
		self.dig = dig

	def __iter__(self):
		return self

	def __next__(self):
		if self.dig:
			n = self.n % 2
			self.n //= 2
			self.dig -= 1
			return bool(n)
		else:
			raise StopIteration()

def test(b, n, queue):
	p = len(list(filter(pos, queue)))
	input = f"{b},{p},{len(queue)-p},{n}"
	args = "\n" + "\n".join(map(str, queue))
	input = (input + args).encode()
	c  = subprocess.run(["./a.out"], input=input, capture_output=True)
	py = subprocess.run(["python", "pytest.py"], input=input, capture_output=True)
	return c, py

def pad(s, n):
	return s + " " * (n-len(s))

def dual_output(s1, s2):
	assert s1 != s2
	s1 = s1.split("\n")
	s2 = s2.split("\n")

	while len(s1) < len(s2):
		s1.append("")
	while len(s1) > len(s2):
		s2.append("")

	assert s1 != s2
	assert len(s1) == len(s2)
	assert any(map(lambda x: x[0] != x[1], zip(s1, s2)))

	for l1, l2 in zip(s1, s2):
		if l1 == l2:
			print(l1)
		else:
			print("\u001b[41m", pad(l1, 59), " ", l2, "\u001b[m", sep="")

b, p, n = sys.argv[1:]
b = int(b)
p = int(p)
n = int(n)

x = ((b+1) * n * ((1<<(p+1)) - 2))
t = tqdm(total=x)
for i in range(1,p+1):
	for j in range(b+1):
		for k in range(1,n+1):
			for l in range(1<<i):
				A = 1
				B = 1
				q = []
				for m in bool_it(l, i):
					if m:
						q.append(A)
						A += 1
					else:
						q.append(-B)
						B += 1
				c, py = test(j, k, q)
				if c.stdout != py.stdout:
					p = len(list(filter(pos, q)))
					input = f"{j},{p},{len(q)-p},{k}"
					args = "\n" + "\n".join(map(str, q))

					print(f"Failed testcase: {repr(input + args)}")
					dual_output(c.stdout.decode(), py.stdout.decode())


					if c.returncode:
						print("There was an error in the c file")
						print(c)
					if py.returncode:
						print("There was an error in the python file")
						print(py)
#					assert not c.returncode,  c
#					assert not py.returncode, p

					if CREATE_NEW_TESTS:
						files = listdir('testsP3-330')
						FILE_NUM = 1
						while f'test_{FILE_NUM}.txt' in files:
							FILE_NUM += 1
						with open(f'testsP3-330/test_{FILE_NUM}.txt', 'w') as file:
							file.write(input + args);
						with open(f'testsP3-330/test_{FILE_NUM}.txt.expected', 'w') as file:
							file.write(py.stdout.decode())
				t.update(1)
