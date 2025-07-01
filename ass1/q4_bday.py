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


# Helper function
def generate_hash() -> tuple[str, bytes]:
    hf1 = sha1(usedforsecurity=True)
    n1 = int(random.random() * MAX_INT_VAL)
    m1 = hex(n1)
    hf1.update(m1.encode("latin-1"))
    h1 = hf1.digest()[:BYTES_NEEDED]
    return m1, h1


"""
Return (m1, m2, numCalls)
"""
# Use the notion of the birthday collision


def q4() -> tuple[str, str, int]:
    # Store the (hash,message) in a table
    table: dict[bytes, str] = {}
    calls = 0
    m2 = b""
    m1 = b""
    while True:
        m1, h1 = generate_hash()
        val = table.get(h1)
        if val == None:
            table[h1] = m1
        # Don't consider trivial H(m1) = H(m1)
        elif m1 == val:
            continue
        # Now we're talkin: H(m1) = H(m2)
        else:
            print("Collision Found!")
            m2 = m1
            break

        calls += 1
    m1 = val
    print("(Hash, m1, m2, calls)")
    print((h1, m1, m2, calls))
    return (m1, m2, calls)


q4()
