# https://github.com/coverslide/node-alea/blob/master/alea.js
# https://github.com/dworthen/prng
from math import floor
from typing import Union, Optional


def rshift(val, n): return (val % 0x100000000) >> n


class AleaState(list[float]):
    pass


class Alea:
    s0 = 0
    s1 = 0
    s2 = 0
    c = 1

    def __init__(self, args: Union[str, AleaState]):
        if isinstance(args, str):
            mash = Mash()
            self.s0 = mash.mash_func(" ")
            self.s1 = mash.mash_func(" ")
            self.s2 = mash.mash_func(" ")

            for i in range(len(args)):
                self.s0 -= mash.mash_func(args[i])
                if self.s0 < 0:
                    self.s0 += 1

                self.s1 -= mash.mash_func(args[i])
                if self.s1 < 0:
                    self.s1 += 1

                self.s2 -= mash.mash_func(args[i])
                if self.s2 < 0:
                    self.s2 += 1
        else:
            self.import_state(args)

    def rnd(self, decimal: Optional[int]):
        t = 2091639 * self.s0 + self.c * 2.3283064365386963e-10  # 2^-32
        self.s0 = self.s1
        self.s1 = self.s2
        self.c = int(t)
        self.s2 = t - self.c
        return self.s2 if decimal is None else floor(self.s2 * decimal)

    # /*
    #   uint32() {
    #       return this.random() * 0x100000000; // 2^32
    #   }
    #
    #   fract53() {
    #       return (
    #           this.random() +
    #           ((this.random() * 0x200000) | 0) * 1.1102230246251565e-16
    #       ); // 2^-53
    #   }
    #   */

    def export_state(self) -> AleaState:
        return AleaState([self.s0, self.s1, self.s2, self.c])

    def import_state(self, params: AleaState):
        self.s0 = +params[0] or 0
        self.s1 = +params[1] or 0
        self.s2 = +params[2] or 0
        self.c = +params[3] or 0


class Mash:
    # mash.version = 'Mash 0.9';
    n: Union[int, float] = 0xefc8249d

    def mash_func(self, data: str):
        for i in range(len(data)):
            self.n += ord(data[i])
            h = 0.02519603282416938 * self.n
            self.n = int(h)
            h -= self.n
            h *= self.n
            self.n = int(h)
            h -= self.n
            self.n += h * 0x100000000  # 2^32

        return int(self.n) * 2.3283064365386963e-10  # 2^-32
