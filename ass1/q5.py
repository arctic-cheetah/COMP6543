import math
import re
import string
from scipy.stats import chisquare
from n_gram_attack import QuadGramAttack
from spellchecker import SpellChecker

letterFrequency = {
    "E": 12.0,
    "T": 9.10,
    "A": 8.12,
    "O": 7.68,
    "I": 7.31,
    "N": 6.95,
    "S": 6.28,
    "R": 6.02,
    "H": 5.92,
    "D": 4.32,
    "L": 3.98,
    "U": 2.88,
    "C": 2.71,
    "M": 2.61,
    "F": 2.30,
    "Y": 2.11,
    "W": 2.09,
    "G": 2.03,
    "P": 1.82,
    "B": 1.49,
    "V": 1.11,
    "K": 0.69,
    "X": 0.17,
    "Q": 0.11,
    "J": 0.10,
    "Z": 0.07,
}
# Global variables
spellCheck = SpellChecker()
TOLERANCE = 0.99
letterFrequency = dict(
    sorted(letterFrequency.items(), key=lambda key_value: key_value[0], reverse=False)
)
# print(letterFrequency)
letterFrequency = [v / 100 for k, v in letterFrequency.items()]

# For example:
# Input Ciphertext: iq q jed l eqvlo wh qy zep ivpzaxhtvi aoftf fe ywpweyag
# Input length of key: 5
# Output Key: alice
# Output Plaintext: if i had a world of my own everything would be nonsense


# Helper functions:
def decrypt_txt(cipher_txt, key):
    decrypted_txt = ""
    i = 0
    for c in cipher_txt:
        if c.isalpha():
            decrypted_char = chr(((ord(c) - ord(key[i])) % 26) + ord("A"))
            decrypted_txt += decrypted_char
            i = (i + 1) % len(key)
        else:
            decrypted_txt += c
    return decrypted_txt


# @Deprecated
def block_list_to_freq(block_list, num_times):
    for x in range(0, len(block_list)):
        tb = block_list[x]
        # num_items = len(tb)
        for k, v in tb.items():
            tb[k] = v / num_times * 100
        # Then sort each table based on the digit
        block_list[x] = dict(
            sorted(tb.items(), key=lambda key_value: key_value[1], reverse=True)
        )
    print(block_list)


# We assume the cipher text only contains alphabets
def key_block_freq(cipher_txt, block_list) -> int:
    block_list_len = len(block_list)
    i = 0
    for x in cipher_txt:
        freq_table = block_list[i]
        if x.isalpha():
            if freq_table.get(x) == None:
                freq_table[x] = 1
            else:
                freq_table[x] = freq_table.get(x) + 1
        i = (i + 1) % block_list_len
    return i


# Apply the shift to each block of the vignere cipher
def apply_shift(block_list) -> list[str]:
    key = []
    for tb in block_list:
        observations = [tb.get(chr(i + 65), 0) for i in range(0, 26)]
        numCharsInBlock = sum(observations)
        bestChi = 0xFFFF_FFFF
        bestShift = 0
        blockLetterFreq = [x * numCharsInBlock for x in letterFrequency]

        for x in range(0, 26):
            # Perform the 'undo' operation. Which is a left rotation
            rotation = observations[x:] + observations[:x]
            # NOTE: Estimator below!
            chiVal = chisquare(rotation, f_exp=blockLetterFreq, sum_check=False)
            # chiVal = [
            #     sum(
            #         (rotation[i] - blockLetterFreq[i]) ** 2 / (letterFrequency[i])
            #         for i in range(0, 26)
            #     )
            # ]

            if chiVal[0] < bestChi:
                bestChi = chiVal[0]
                bestShift = x

        key.append(chr(65 + bestShift))
    return key


# -------------------------------------------------------------------------


# TODO:
# Your task is design and implement an algorithm that takes as input a Vigenere
# ciphertext and length of the key and generates the plaintext message as output.
def chi_square_attack(cipher_txt: str, key_len: int):
    print("1) Performing Chi-Squared Frequency Analysis Attack")
    block_list: list[dict[str, int]] = []
    cipher_txt = cipher_txt.upper()
    cipher_txt_no_space = re.sub(r"[^A-Za-z]", "", cipher_txt)
    # num_times = math.floor(len(cipher_txt) / key_len)

    for _ in range(0, key_len):
        block_list.append({})

    # print(cipher_txt)
    # print(cipher_txt_no_space)
    # Convert each char into their respective blocks
    key_block_freq(cipher_txt_no_space, block_list)
    # print(block_list)

    # Now for each block we should smart 'brute force' as it's basically
    # just a caesar shift to
    # find the characters that
    # match the frequency using
    # Perform a chi-squared-test
    # We'll rotate firt
    key = apply_shift(block_list)
    decrypted_txt = decrypt_txt(cipher_txt, key)
    # print((key, decrypted_txt))
    return (key, decrypted_txt)


def word_score(plain_txt: str):
    # Determine, if the plain text has been deciphered properly.
    words = re.findall(r"[A-Za-z]{2,}", plain_txt.upper())
    unknown_words = spellCheck.unknown(words)
    print(unknown_words)
    accuracy = 1 - len(unknown_words) / len(words)
    print(
        "Using spell check, the accuracy of the cracked text is: "
        + str(round(accuracy * 100, 3))
        + "%"
    )
    return accuracy


def quad_gram_attack(cipher_txt, key_len):
    breaker = QuadGramAttack(cipher_txt, key_len)
    best_key, best_e = breaker.anneal()
    best_key = [string.ascii_uppercase[k] for k in best_key]
    print("\n")
    plain_txt = decrypt_txt(cipher_txt, best_key)
    return best_key, plain_txt


def obtain_key(plain_txt: str, cipher_txt: str, key_len: int) -> list[str]:
    plain_txt_cleaned = re.sub(r"[^A-Za-z]", "", plain_txt)
    cipher_txt_cleaned = re.sub(r"[^A-Za-z]", "", cipher_txt)

    t1 = plain_txt_cleaned[0:key_len]
    t2 = cipher_txt_cleaned[0:key_len]
    key = []
    for x in range(0, key_len):
        key.append(chr((ord(t2[x]) - ord(t1[x])) % 26 + ord("A")))

    return key


def attack_path(cipher_txt: str, key_len: int):
    # If ciphertext is less than 300 chars, then perform quad-gram hill ascent attack

    # Otherwise, use Chi-square attack with quad-gram attack, then polish attack
    # with quad-gram hill.
    cipher_txt = cipher_txt.upper()
    cipher_txt_len = len(re.sub(r"[^a-zA-Z]", "", cipher_txt))

    if cipher_txt_len > 250:
        best_key, plain_txt = chi_square_attack(cipher_txt, key_len)
    else:
        best_key, plain_txt = quad_gram_attack(cipher_txt, key_len)
    print(f"'Best' key result: {best_key}")
    print(f"'Best' cracked text result: {plain_txt}\n")

    # Finally verify with spell checker
    accuracy = word_score(plain_txt)
    if accuracy < TOLERANCE:
        print(f"Do you accept the accuracy of: {round(accuracy * 100, 3)}? Y or N")
        res = input()
        print()
        if res.lower() == "y":
            print(f"The 'best' key is: {best_key}")
            print(f"The cracked cipher text is: {plain_txt}")
        else:
            print(f"Do not accept the estimated result.  Refine attack with:")
            _, plain_txt = quad_gram_attack(plain_txt, key_len)
            best_key = obtain_key(plain_txt, cipher_txt, key_len)
    else:
        print(f"Accuracy exceeds {TOLERANCE * 100}%!")

    print(f"The 'best' key is: \n{best_key}\n")
    print(f"The cracked cipher text is: \n{plain_txt}")
    print("_______________________________________________________________")

    return (best_key, plain_txt)


if __name__ == "__main__":

    # Anneal attack
    # attack_path(
    #     "Vyc fnqkm spdpv nqo hjfxa qmcg 13 eiha umvl. Jcv zr sbl vqk jxdm jgzlv mmiuvb qr bpg frwxz nqoch Ucb yyw sbl qv um hh? Em orw cxdmt bldp! Jcv nfpm Q kce qpr qa vyyi pm ajfsaw vwv sc bxiv ceb zbvl. Uymjel eg sc shqvi dmgx wn vygh dqvf fd pgitajgh?",
    #     7,
    # )
    cipher = "Vyc fnqkm spdpv nqo hjfxa qmcg 13 eiha umvl. Jcv zr sbl vqk jxdm jgzlv mmiuvb qr bpg frwxz nqoch. Lw qv smjzpb ufkt uqo fzjsha ipu dxetmf zr ji eqvy kxes. Jwk uwr lqf zr sh aw? Dvapnam kk upgbmf mcczmiptc pgl lgtgsxl bjrr iam jgjr ltg bq icrhuxgeqt mpmo nyh mw ucbc xm kco fl pet bjv miamz dze bxivkvq. Pl acey yae bpg wmmxa avfnexl bgrqxgo bjvk pgl bjvw gxaxgtrtw bpgd ldp. Vwy kft ywf yrq gxdmtvb qr mdgiwdgm, ipu rwxg tkmcs aixrzjn xdmt rdixz"
    attack_path(cipher, 7)

    # attack_path("iq q jed l eqvlo wh qy zep ivpzaxhtvi aoftf fe ywpweyag", 5)
    # attack_path(
    #     "Php bmecv mjkwy qgt jfxho ogpj 13 hakj vkgd. Mmp ie oaz nze dekp mwenr ewwspo tu tsp gphpc xkxpd Tqt hsq zio tl zo dz?",
    #     5,
    # )


# 293 chars long below
# attack_path(
#     "Vyc fnqkm spdpv nqo hjfxa qmcg 13 eiha umvl. Jcv zr sbl vqk jxdm jgzlv mmiuvb qr bpg frwxz nqoch, lw qv xmi lwug dgad ivf tsbfml ccj domz vycb! Ucb yyw sbl qv um hh? Em orw cxdmt bldp! Jcv nfpm Q kce qpr qa vyyi pm ajfsaw vwv sc bxiv ceb zbvl. Uymjel eg sc shqvi dmgx wn vygh dqvf fd pgitajgh?",
#     7,
# )

# 246 characters below


# attack_path(
#     "BYOIZRLAUMYXXPFLPWBZLMLQPBJMSCQOWVOIJPYPALXCWZLKXYVMKXEHLIILLYJMUGBVXBOIRUAVAEZAKBHXBDZQJLELZIKMKOWZPXBKOQALQOWKYIBKGNTCPAAKPWJHKIAPBHKBVTBULWJSOYWKAMLUOPLRQOWZLWRSLEHWABWBVXOLSKOIOFSZLQLYKMZXOBUSPRQVZQTXELOWYHPVXQGDEBWBARBCWZXYFAWAAMISWLPREPKULQLYQKHQBISKRXLOAUOIEHVIZOBKAHGMCZZMSSSLVPPQXUVAOIEHVZLTIPWLPRQOWIMJFYEIAMSLVQKWELDWCIEPEUVVBAZIUXBZKLPHKVKPLLXKJMWPFLVBLWPDGCSHIHQLVAKOWZSMCLXWYLFTSVKWELZMYWBSXKVYIKVWUSJVJMOIQOGCNLQVXBLWPHKAOIEHVIWTBHJMKSKAZMKEVVXBOITLVLPRDOGEOIOLQMZLXKDQUKBYWLBTLUZQTLLDKPLLXKZCUKRWGVOMPDGZKWXZANALBFOMYIXNGLZEKKVCYMKNLPLXBYJQIPBLNMUMKNGDLVQOWPLEOAZEOIKOWZZMJWDMZSRSMVJSSLJMKMQZWTMXLOAAOSTWABPJRSZMYJXJWPHHIVGSLHYFLPLVXFKWMXELXQYIFUZMYMKHTQSMQFLWYIXSAHLXEHLPPWIVNMHRAWJWAIZAAWUGLBDLWSPZAJSCYLOQALAYSEUXEBKNYSJIWQUKELJKYMQPUPLKOLOBVFBOWZHHSVUIAIZFFQJEIAZQUKPOWPHHRALMYIAAGPPQPLDNHFLBLPLVYBLVVQXUUIUFBHDEHCPHUGUM",
#     6,
# )

# attack_path(
#     "NEIWUGJJOPCTWTBMJCKAGLDRETBBFKHGNPMLDONEFOLXJCLJKTZWDZDKNMNRQIFQRUBLVVBMEBZQRZKNDAAUIVVVGUJZCMBAHRNSWYKUIJCMWTOWRKHRDBQSAGIQLMXENMLJETBLMCJNZZYRZJMWNYKLMIGTWTYBFKOZVOLGJZVQPUBZCMBGUICILMAJDVRUWLDBDAHHMMCFACCQANLRVGCJWHJCRZDKDZDGYKNBFKMADKIYERQMPECRVHCUJZCMPORKMAYTZVJWJYRGIQQNAJAZMSXXJIBSEXMWPYKLGQENPZCMWIDGIOCJPUGCQZNKGMQYONZMRYKLGMYJSOOPYYQXAIAKHOFMYXWYKJSZPNVBQVAIOIARAJDLLUPGANCIPNZZNXAUXKSVWZDWLNAXXWSTPKIILIAGIIRANGGKYXJGOQMTORDOFZHEZUZXKCIMBHUZCMQKWYJVFGZJZMNKJKYQRYPOIOCCEZCBFKXKVBGTCUABFKNGDVBXKVNILJDKMPYONCCQANPNZXPKOYPZCUBZCMAUSYATYTGYCIBGOANCYRYGPACJPUOCKHHKYWUTBXJUGZOLVARKJOIOQGJJNBPGUHZGMTZZCMAANZVQLUBNZZAGHOXWZUJTZBUGOSVLCIHGHUWHUZCMKUEYOCPKPOGTGZDGMLJESGNJCZPKMBFGJYZIUKAJDWSMDZIWRZKNVDCIKSZQQALVJACYDKHCPSQXZLJUKQDVEGPZCMQQUOVUQUNXTNMXPNZZYOJYVQBNAHPBFUSMGIBOWSOWFGRKTWSNAXZZCSKZZMEJKTYQQGLVZIPKZHTLCMNKZJCNETYBFKHOLCGJ",
#     6,
# )
