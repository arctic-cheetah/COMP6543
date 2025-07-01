import re, math, collections

ENG_FREQ = [
    8.12,  # A, adjust if you want more precise %
    1.49,  # B
    2.71,  # C
    4.32,  # D
    12.0,  # E
    2.30,  # F
    2.03,  # G
    5.92,  # H
    7.31,  # I
    0.10,  # J
    0.69,  # K
    3.98,  # L
    2.61,  # M
    6.95,  # N
    7.68,  # O
    1.82,  # P
    0.11,  # Q
    6.02,  # R
    6.28,  # S
    9.10,  # T
    2.88,  # U
    1.11,  # V
    2.09,  # W
    0.17,  # X
    2.11,  # Y
    0.07,  # Z
]
ENG_FREQ = [f / 100 for f in ENG_FREQ]  # to fractions


def chi_square_shift(block):
    """Return the shift (0–25) with smallest χ² for this block."""
    N = len(block)
    if not N:
        return 0
    # raw counts for the ciphertext block
    counts = collections.Counter(block)
    obs = [counts.get(chr(i + 65), 0) for i in range(26)]

    best_s, best_chi = 0, float("inf")
    for s in range(26):
        # decrypt by shift s: rotate counts *backwards* by s
        rotated = obs[s:] + obs[:s]  #  e.g. s=1 moves A-count to B slot
        chi = sum(
            (rotated[i] - ENG_FREQ[i] * N) ** 2 / (ENG_FREQ[i] * N) for i in range(26)
        )
        if chi < best_chi:
            best_s, best_chi = s, chi
    return best_s  # 0→A, 1→B, …


def recover_key(cipher_txt: str, key_len: int):
    cipher_txt = re.sub(r"[^A-Za-z]", "", cipher_txt).upper()
    blocks = ["".join(cipher_txt[i::key_len]) for i in range(key_len)]
    shifts = [chi_square_shift(b) for b in blocks]
    key = "".join(chr(65 + s) for s in shifts).lower()  # lower-case like example
    return key


def decrypt_vigenere(cipher_txt: str, key: str):
    res = []
    key = key.upper()
    j = 0
    for c in cipher_txt.upper():
        if not c.isalpha():
            res.append(c)
            continue
        shift = ord(key[j % len(key)]) - 65
        p = (ord(c) - 65 - shift) % 26
        res.append(chr(p + 65))
        j += 1
    return "".join(res).lower()


# Demo
# cipher = "iq q jed l eqvlo wh qy zep ivpzaxhtvi aoftf fe ywpweyag"

cipher = "Vyc fnqkm spdpv nqo hjfxa qmcg 13 eiha umvl. Jcv zr sbl vqk jxdm jgzlv mmiuvb qr bpg frwxz nqoch, lw qv xmi lwug dgad ivf tsbfml ccj domz vycb! Ucb yyw sbl qv um hh? Em orw cxdmt bldp! Jcv nfpm Q kce qpr qa vyyi pm ajfsaw vwv sc bxiv ceb zbvl. Uymjel eg sc shqvi dmgx wn vygh dqvf fd pgitajgh?"

klen = 7
key = recover_key(cipher, klen)  # → 'alice'
plain = decrypt_vigenere(cipher, key)

print("Key :", key)
print("Text:", plain)
