from .. import algorithm as algo

class PKC:

    def __init__(self):
        pass

    def encrypt(self, m):
        if type(m) == str:
            nums = algo.to_num(m)
            return list(map(self._encrypt, nums))
        else:
            return self._encrypt(m)

    def decrypt(self, carr):
        if type(carr) == list:
            marr = list(map(self._decrypt, carr))
            return algo.to_str(marr)
        else:
            return self._decrypt(carr)

    def _encrypt(self, m):
        return 0

    def _decrypt(self, c):
        return 0