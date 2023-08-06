from .. import algorithm as algo
from .pkc_template import PKC
import random

__all__ = ["GoldwasserMicaliPKC"]

class GoldwasserMicaliPKC(PKC):

    def __init__(self, p, q):
        self.p = p
        self.q = q
        x = 2
        while True:
            if algo.is_non_residue(x, p) and algo.is_non_residue(x, q):
                break
            x += 1
        self.a = x
        self.N = p * q

    def encrypt(self, m):
        return super().encrypt(m)

    def decrypt(self, n):
        return super().decrypt(n)

    def _encrypt(self, m):
        nums = bin(m)[2:]
        return tuple(map(self._encrypt_helper, nums))

    def _decrypt(self, carr):
        string = "".join(list(map(self._decrypt_helper, carr)))
        return int(string, 2)
        
    def _encrypt_helper(self, m):
        if type(m) == str:
            m = int(m)
        r = random.randint(3, self.N - 1)
        if m == 0:
            return r * r % self.N
        else:
            return (self.a * r * r) % self.N

    def _decrypt_helper(self, m):
        ## Sometimes exactly one of them equal 0
        if algo.is_non_residue(m, self.p) or algo.is_non_residue(m, self.q):
            return "1"
        return "0"

        