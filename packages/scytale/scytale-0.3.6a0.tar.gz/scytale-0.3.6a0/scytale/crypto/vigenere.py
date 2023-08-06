from .. import algorithm as algo

__all__ = ['Vigenere']

LENGTH = 126

class Vigenere:

    def __init__(self, key=""):
        if len(key) == 0:
            self.key = algo.to_num("A")
        else:
            self.key = algo.to_num(key.upper())
        self.len = len(self.key)
    
    def encrypt(self, text):
        nums = algo.to_num(text)
        n = self.len
        result = [(nums[i] + self.key[i % n]) % LENGTH for i in range(len(nums))]
        return algo.to_str(result)

    def decrypt(self, text):
        nums = algo.to_num(text)
        n = self.len
        result = [(nums[i] - self.key[i % n]) % LENGTH for i in range(len(nums))]
        return algo.to_str(result)