from base64 import b64encode, b64decode
import random
from  AES import BLOCK_LENGTH, xor_with_key, permutation, substitution
import os
FILE = 'output.txt'
FILE = os.path.join(os.path.dirname(__file__), FILE)


def main():
    cypertext = ''
    with open(FILE, 'r') as f:
        ciphertext = f.read().strip()
    b64 = b64decode(ciphertext)
    # print(b64)
    # print(bytes(b64))

    
    blocks = []
    for i in range(len(b64) - BLOCK_LENGTH, -1, -BLOCK_LENGTH):
        blocks.append(b64[i:i+BLOCK_LENGTH])
    
    for key in [b'\x00\x00', b'\x00\x01', b'\x01\x00', b'\x01\x01']:
        random.seed(key)
        key_expanded = random.getrandbits(BLOCK_LENGTH*8).to_bytes(BLOCK_LENGTH, 'big')

        output = ""
        for block in blocks:
            block = xor_with_key(block, key_expanded)
            block = permutation(block)
            block = substitution(block)
            block = xor_with_key(block, key_expanded)
            output+= "".join([chr(char) for char in block])
        print(output)


if __name__ == "__main__":
    main()