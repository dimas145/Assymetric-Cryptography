from .utils import Utils
from random import randrange

import math


class Paillier:
    def _lcm(self, a, b):
        return abs(a * b) // math.gcd(a, b)

    def _L(self, x, n):
        return (x - 1) / n

    def generate_keys(self, p, q):
        # TODO check gcd(pq, (p-1)(q-1)) = 1
        n = p * q
        lamb = self._lcm(p - 1, q - 1)
        g = randrange(n * n)
        mu = pow(self._L(pow(g, lamb, n * n), n), -1)

        # private key = (lamb, mu)
        # public key = (g, n)
        return g, n, lamb, mu

    def encrypt(self, m, g, n, r=0):
        while math.gcd(r, n) != 1:
            r = randrange(n)

        return (pow(g, m) * pow(r, n)) % (n * n)

    def decrypt(self, c, n, lamb, mu):
        return int((self._L(pow(c, lamb, n * n), n) * mu) % n)
