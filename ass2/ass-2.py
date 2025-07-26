import math


# p,q are prime and q | (p - 1)
def algo1(p, q):
    for x in range(p):
        if x**q % p == 0:
            return x


def algo2(p, q):
    for x in range(p):
        if x ** ((p - 1) / q) % p == 0:
            return x
