RANMGE = (ord('Z') - ord('A') + 1) % (26) + ord('A')
NUM_ALPHABET = 26
def shift_text(plaintext: str, shift : int) -> str:
    # Given a plaint text in all capitals
    # Shift each character by shift places
    cipherText = ""
    for c in plaintext:
        res = (ord(c) + shift - ord('A')) % 26 + ord('A')
        cipherText += chr(res)
    return cipherText

def decipher(ciphertext: str, shift : int) -> str:
    plainText = ""
    for c in ciphertext:
        res = (ord(c) - shift - ord('A')) % 26 + ord('A')
        plainText += chr(res)
    return plainText    

def main():
    use = print(shift_text("Hello".upper(), 5))
    print(shift_text("DGHLTEWQ", 5))
    print(decipher(shift_text("DGHLTEWQ", 5), 5))

if __name__ == "__main__":
    main()
