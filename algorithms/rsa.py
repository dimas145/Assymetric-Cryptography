from .utils import Utils

import math
import re


class RSA:
    def generate_keys(self, p, q, e):
        n = p * q
        phi = (p - 1) * (q - 1)

        d = self._multiplicative_inverse(e, phi)

        # private key = (d, n)
        # public key = (e, n)
        return n, e, d

    def _multiplicative_inverse(self, e, phi):
        return self._extended_euclid(e, phi)[1] % phi

    def _extended_euclid(self, a, b):
        if b == 0:
            return a, 1, 0

        d, x2, y2 = self._extended_euclid(b, a % b)
        x, y = y2, x2 - (a // b) * y2
        return d, x, y

    def _preprocess(self, text):
        text = re.sub(r'[^a-zA-Z]', '', text).upper()
        return ''.join(str(ord(c) - 65).zfill(2) for c in text)

    def encrypt(self, text, e, n):
        text = self._preprocess(text)

        block_size = 4
        encrypted = ""
        for i in range(0, len(text), block_size):
            m = int(text[i:i + block_size])
            c = pow(m, e, n)
            encrypted += str(c).zfill(block_size)

        return encrypted

    def decrypt(self, text, d, n):
        block_size = 4
        decrypted = ""
        for i in range(0, len(text), block_size):
            c = int(text[i:i + block_size])
            m = pow(c, d, n)
            decrypted += str(m).zfill(block_size)

        text = ""
        for i in range(0, len(decrypted), 2):
            text += chr(int(decrypted[i:i + 2]) + 65)

        return text
