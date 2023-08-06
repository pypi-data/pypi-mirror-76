from .. import algorithm as algo
from .pkc_template import PKC
import numpy as np

__all__ = ['RSA']

class RSA(PKC):

    def __init__(self, e, p, q):
        assert(algo.gcd(e, (p - 1) * (q - 1)) == 1)
        self.e = e
        self.p = p
        self.q = q
        self.d = algo.inverse_mod(e, (p - 1) * (q - 1))
        self.N = p * q
    
    def encrypt(self, text):
        return super().encrypt(text)

    def decrypt(self, carr):
        return super().decrypt(carr)

    def _encrypt(self, m):
        return pow(m, self.e) % self.N

    def _decrypt(self, c):
        return pow(c, self.d) % self.N