import random, re
import string
from simanneal import Annealer
from ngram_score import NGramScore


# 1️⃣Build a quad-gram model from english_quadgrams.txt (James Lyons data)
quad = NGramScore("quadgrams.txt")


# 2️⃣Use simulated annealing to attack the Vigenère (unchanged apart from scorer)
class QuadGramAttack(Annealer):
    def __init__(self, cipher_txt: str, key_len: int):
        self.cipher = re.sub("[^A-Z]", "", cipher_txt.upper())
        super().__init__([random.randint(0, 25) for _ in range(key_len)])
        print("2) Performing the Quad-Gram Hill Ascent Attack")

    def move(self):
        # Tweak the key
        i = random.randrange(len(self.state))
        self.state[i] = (self.state[i] + random.randint(1, 25)) % 26

    def energy(self):
        pt = "".join(
            chr(((ord(c) - 65 - self.state[i % len(self.state)]) % 26) + 65)
            for i, c in enumerate(self.cipher)
        )
        # 3️⃣ Search for the lowest energy state with the annealer and quad-gram
        return -quad.score(pt)


# --- Test -------------------------------------------------

# cipher_txt = "Vyc fnqkm spdpv nqo hjfxa qmcg 13 eiha umvl. Jcv zr sbl vqk jxdm jgzlv mmiuvb qr bpg frwxz nqoch, lw qv xmi lwug dgad ivf tsbfml ccj domz vycb! Ucb yyw sbl qv um hh? Em orw cxdmt bldp! Jcv nfpm Q kce qpr qa vyyi pm ajfsaw vwv sc bxiv ceb zbvl. Uymjel eg sc shqvi dmgx wn vygh dqvf fd pgitajgh?"
# cipher_txt = "Vyc fnqkm spdpv nqo hjfxa qmcg 13 eiha umvl. Jcv zr sbl vqk jxdm jgzlv mmiuvb qr bpg frwxz nqoch, lw qv xmi lwug dgad ivf tsbfml ccj domz vycb! Ucb yyw sbl qv um hh? Em orw cxdmt bldp! Jcv nfpm Q kce qpr qa vyyi pm ajfsaw vwv sc bxiv ceb zbvl. Uymjel eg sc shqvi dmgx wn vygh dqvf fd pgitajgh?"
# cipher_txt = "Vyc fnqkm spdpv nqo hjfxa qmcg 13 eiha umvl. Jcv zr sbl vqk jxdm jgzlv mmiuvb qr bpg frwxz nqoch Ucb yyw sbl qv um hh? "
# cipher_txt = "Php bmecv mjkwy qgt jfxho ogpj 13 hakj vkgd. Mmp ie oaz nze dekp mwenr ewwspo tu tsp gphpc xkxpd Tqt hsq zio tl zo dz?"
# key_len = 5


# breaker = QuadGramAttack(cipher_txt, key_len)
# best_key, best_e = breaker.anneal()
# print("Key:", "".join(string.ascii_uppercase[k] for k in best_key))
