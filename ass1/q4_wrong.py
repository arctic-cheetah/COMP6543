from hashlib import sha1
import random

# Write a program to find hash collisions on a 40-bit hash  (5 bytes). The program should
# consist of a function hashCollision() that returns a tuple (m1, m2, n),
# where m1 and m2 are different ASCII strings whose SHA-1 hashes have the same highorder 40 bits (same 10 initial hex digits).
# The component n of the return value
# is the number of calls to SHA-1. You can generate random ASCII strings by
# converting random integers to hex.

"""
Return (m1, m2, numCalls)
"""
MAX_INT_VAL = 0xFFFF_FFFF
BYTES_NEEDED = int(40 / 8)


def hashCollision() -> tuple[str, str, int]:
    hf1 = sha1(usedforsecurity=False)
    n1 = int(random.random() * MAX_INT_VAL)
    m1 = hex(n1).encode("latin-1")
    hf1.update(m1)
    h1 = hf1.digest()[:BYTES_NEEDED]
    print(h1.hex())

    i = 0
    calls = 1
    # hf2 = sha1(usedforsecurity=False)
    # m2 = hex(i).encode("latin-1")
    # hf2.update(m2)
    # h2 = hf2.digest()[:BYTES_NEEDED]

    while True:
        hf2 = sha1(usedforsecurity=False)
        m2 = hex(i).encode("latin-1")
        hf2.update(m2)
        h2 = hf2.digest()[:BYTES_NEEDED]
        if h1 == h2:
            break
        if i > 1048576:
            print(i)
        #     print(m2)
        #     print(h2)

        i += 1
        calls += 1

    print((m1.hex(), m2.hex(), calls))
    return (m1.hex(), m2.hex(), calls)


print(hashCollision())
