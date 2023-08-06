from random import randint
from Cryptodome.Util import number

__import__('sys').setrecursionlimit(10000)
class PublicKey():
	def __init__(self, p, g, y):
		self.p = p
		self.g = g
		self.y = y

	def __str__(self):
		return f'PublicKey({self.p}, {self.g}, {self.y})'
		
	def get(self):
		return self.p, self.g, self.y

class PrivateKey():
	def __init__(self, p, x):
		self.p = p
		self.x = x
		

	def __str__(self):
		return f'PrivateKey({self.p}, {self.x})'
		
	def get(self):
		return (self.p, self.x)

class CipherText():
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def __str__(self):
		return f'CipherText({self.a}, {self.b})'

	def get(self):
		return (self.a, self.b)


class Elgamal():
	def binpow(a, n, m):
		if n == 0:
			return 1
		if n % 2 == 1:
			return Elgamal.binpow(a, n-1, m) * a % m
		else:
			b = Elgamal.binpow(a, n // 2, m) % m
			return b * b

	def get_g(p):
		p1 = p - 1
		d = (p-1) // 2

		j = 2
		while j < p-1:

			# print(f'j:{j} d:{d} p:{p}') 
			g1 = Elgamal.binpow(j, d, p)
			if g1 == p1: 
				return j

			if j > 100:
				return 0
			j += 1

		return 0 

	def newkeys(n_lenth):

		g = 0

		while g == 0:
			p = number.getPrime(n_lenth  * 16, __import__('os').urandom)
			g = Elgamal.get_g(p)

		x = randint(1, p-1)
		y = Elgamal.binpow(g, x, p)

		pv = PrivateKey(p, x)
		pb = PublicKey(p, g, y)

		return pb, pv

	def encrypt(data, pb):
		M = int(data.hex(), 16)
		p, g, y = pb.get()

		# print(f'M:{M}, p:{p}')

		if M >= p:
			raise Exception('Data is so big (data > p)')

		k = randint(1, p-1)

		a = Elgamal.binpow(g, k, p)
		b = Elgamal.binpow(y, k, p) * M % p

		ct = CipherText(a, b)

		return ct

	def decrypt(ct, pv):
		a, b = ct.get()
		p, x = pv.get()

		dd = Elgamal.binpow(a, (p - 1 - x), p) * b % p

		h = hex(dd)[2:]
		h = h if len(h) % 2 == 0 else '0' + h
		dd = bytearray.fromhex(h)
		return dd
