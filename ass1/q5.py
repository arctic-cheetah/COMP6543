import collections
import re, math
from scipy.stats import chisquare

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
letterFrequency = dict(
    sorted(letterFrequency.items(), key=lambda key_value: key_value[0], reverse=False)
)
print(letterFrequency)
letterFrequency = [v / 100 for k, v in letterFrequency.items()]

# print(letterFrequency)
# For example:
# Input Ciphertext: iq q jed l eqvlo wh qy zep ivpzaxhtvi aoftf fe ywpweyag
# Input length of key: 5
# Output Key: alice
# Output Plaintext: if i had a world of my own everything would be nonsense


# TODO:
# Your task is design and implement an algorithm that takes as input a Vigenere
# ciphertext and length of the key and generates the plaintext message as output.
def q5(cipher_txt: str, key_len: int):
    ht_list: list[dict[str, int]] = []
    cipher_txt = cipher_txt.upper()
    cipher_txt_no_space = re.sub(r"[^A-Za-z]", "", cipher_txt)
    # num_times = math.floor(len(cipher_txt) / key_len)

    for _ in range(0, key_len):
        ht_list.append({})

    # print(cipher_txt)
    # print(cipher_txt_no_space)
    key_block_freq(cipher_txt_no_space, ht_list)
    # blocks = ["".join(cipher_txt_no_space[i::key_len]) for i in range(key_len)]

    # print(ht_list)
    # ht_list_to_freq(ht_list, num_times)
    # for x in blocks:
    #     ht_list.append(collections.Counter(x))

    # print(ht_list)

    # Now for each block we should smart 'brute force' as it's basically
    # just a caesar shift to
    # find the characters that
    # match the frequency using
    # Perform a chi-squared-test
    # We'll rotate firt
    key = []
    for tb in ht_list:
        observations = [tb.get(chr(i + 65), 0) for i in range(0, 26)]
        numCharsInBlock = sum(observations)
        bestChi = 0xFFFF_FFFF
        bestShift = 0
        blockLetterFreq = [x * numCharsInBlock for x in letterFrequency]
        # print(numCharsInBlock)
        # print(blockLetterFreq)
        for x in range(0, 26):
            # Perform the 'undo' operation. Which is a left rotation
            rotation = observations[x:] + observations[:x]
            # library is fkn broken for my tolerance!
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
    print(key)

    decrypted_txt = decrypt_txt(cipher_txt, key)
    print(decrypted_txt)

    return key


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


def ht_list_to_freq(ht_list, num_times):
    for x in range(0, len(ht_list)):
        tb = ht_list[x]
        num_items = len(tb)
        for k, v in tb.items():
            tb[k] = v / num_times * 100
        # Then sort each table based on the digit
        ht_list[x] = dict(
            sorted(tb.items(), key=lambda key_value: key_value[1], reverse=True)
        )
    print(ht_list)


# We assume the cipher text only contains alphabets
def key_block_freq(cipher_txt, ht_list) -> int:
    ht_list_len = len(ht_list)
    i = 0
    for x in cipher_txt:
        freq_table = ht_list[i]
        if x.isalpha():
            if freq_table.get(x) == None:
                freq_table[x] = 1
            else:
                freq_table[x] = freq_table.get(x) + 1
        i = (i + 1) % ht_list_len
    return i


# 293 chars long below
# q5(
#     "Vyc fnqkm spdpv nqo hjfxa qmcg 13 eiha umvl. Jcv zr sbl vqk jxdm jgzlv mmiuvb qr bpg frwxz nqoch, lw qv xmi lwug dgad ivf tsbfml ccj domz vycb! Ucb yyw sbl qv um hh? Em orw cxdmt bldp! Jcv nfpm Q kce qpr qa vyyi pm ajfsaw vwv sc bxiv ceb zbvl. Uymjel eg sc shqvi dmgx wn vygh dqvf fd pgitajgh?",
#     7,
# )

q5(
    "The quick brown fox jumps over 13 lazy dogs. But it did not like being teased by the other foxes But why did it do so? We may never know! But what I can say is that we should not be mean and kind. Should we be doing more of this kind of analysis?",
    7,
)

q5("iq q jed l eqvlo wh qy zep ivpzaxhtvi aoftf fe ywpweyag", 5)
# q5(
#     "BYOIZRLAUMYXXPFLPWBZLMLQPBJMSCQOWVOIJPYPALXCWZLKXYVMKXEHLIILLYJMUGBVXBOIRUAVAEZAKBHXBDZQJLELZIKMKOWZPXBKOQALQOWKYIBKGNTCPAAKPWJHKIAPBHKBVTBULWJSOYWKAMLUOPLRQOWZLWRSLEHWABWBVXOLSKOIOFSZLQLYKMZXOBUSPRQVZQTXELOWYHPVXQGDEBWBARBCWZXYFAWAAMISWLPREPKULQLYQKHQBISKRXLOAUOIEHVIZOBKAHGMCZZMSSSLVPPQXUVAOIEHVZLTIPWLPRQOWIMJFYEIAMSLVQKWELDWCIEPEUVVBAZIUXBZKLPHKVKPLLXKJMWPFLVBLWPDGCSHIHQLVAKOWZSMCLXWYLFTSVKWELZMYWBSXKVYIKVWUSJVJMOIQOGCNLQVXBLWPHKAOIEHVIWTBHJMKSKAZMKEVVXBOITLVLPRDOGEOIOLQMZLXKDQUKBYWLBTLUZQTLLDKPLLXKZCUKRWGVOMPDGZKWXZANALBFOMYIXNGLZEKKVCYMKNLPLXBYJQIPBLNMUMKNGDLVQOWPLEOAZEOIKOWZZMJWDMZSRSMVJSSLJMKMQZWTMXLOAAOSTWABPJRSZMYJXJWPHHIVGSLHYFLPLVXFKWMXELXQYIFUZMYMKHTQSMQFLWYIXSAHLXEHLPPWIVNMHRAWJWAIZAAWUGLBDLWSPZAJSCYLOQALAYSEUXEBKNYSJIWQUKELJKYMQPUPLKOLOBVFBOWZHHSVUIAIZFFQJEIAZQUKPOWPHHRALMYIAAGPPQPLDNHFLBLPLVYBLVVQXUUIUFBHDEHCPHUGUM",
#     6,
# )

# q5(
#     "NEIWUGJJOPCTWTBMJCKAGLDRETBBFKHGNPMLDONEFOLXJCLJKTZWDZDKNMNRQIFQRUBLVVBMEBZQRZKNDAAUIVVVGUJZCMBAHRNSWYKUIJCMWTOWRKHRDBQSAGIQLMXENMLJETBLMCJNZZYRZJMWNYKLMIGTWTYBFKOZVOLGJZVQPUBZCMBGUICILMAJDVRUWLDBDAHHMMCFACCQANLRVGCJWHJCRZDKDZDGYKNBFKMADKIYERQMPECRVHCUJZCMPORKMAYTZVJWJYRGIQQNAJAZMSXXJIBSEXMWPYKLGQENPZCMWIDGIOCJPUGCQZNKGMQYONZMRYKLGMYJSOOPYYQXAIAKHOFMYXWYKJSZPNVBQVAIOIARAJDLLUPGANCIPNZZNXAUXKSVWZDWLNAXXWSTPKIILIAGIIRANGGKYXJGOQMTORDOFZHEZUZXKCIMBHUZCMQKWYJVFGZJZMNKJKYQRYPOIOCCEZCBFKXKVBGTCUABFKNGDVBXKVNILJDKMPYONCCQANPNZXPKOYPZCUBZCMAUSYATYTGYCIBGOANCYRYGPACJPUOCKHHKYWUTBXJUGZOLVARKJOIOQGJJNBPGUHZGMTZZCMAANZVQLUBNZZAGHOXWZUJTZBUGOSVLCIHGHUWHUZCMKUEYOCPKPOGTGZDGMLJESGNJCZPKMBFGJYZIUKAJDWSMDZIWRZKNVDCIKSZQQALVJACYDKHCPSQXZLJUKQDVEGPZCMQQUOVUQUNXTNMXPNZZYOJYVQBNAHPBFUSMGIBOWSOWFGRKTWSNAXZZCSKZZMEJKTYQQGLVZIPKZHTLCMNKZJCNETYBFKHOLCGJ",
#     6,
# )
