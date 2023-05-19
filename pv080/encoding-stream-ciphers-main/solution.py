# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# + [markdown] id="t1ppBGhN3AjM"
# # Seminar 03: Mapping, Encoding, Stream Ciphers

# + [markdown] id="kRTb2GLc3AjP"
# ## Mapping

# + [markdown] id="VrPvH51B3AjQ"
# We will encounter many cryptographic functions in this course. Most of them simply transform an input into some output. Your first goal is to try working with such functions, starting with the most simple ones.

# + id="S_NkvJGr3AjS"
def define_mapping(inputs: list, outputs: list):
    """ Returns a FUNCTION which maps the `inputs` to the `outputs`. """
    def mapping(preimage):
        mappinct_as_dict = dict(zip(inputs, outputs))
        image = mappinct_as_dict[preimage]
        return image
    return mapping


# + [markdown] id="SAw1r7DC3AjV"
# Let's see how `define_mapping` works.

# + id="77IoTD3t3AjX" outputId="4beca8c5-d034-4934-f85e-51f702c35072"
mapping = define_mapping(inputs = ['X'], outputs=['F'])
mapping('X')

# + [markdown] id="z5DsXMcZ3AjY"
# **Task 1**: Set `inputs` and `outputs` to create a mapping that maps characters `X, Y, Z` to values `0, 1, 2`.

# + id="QHGFlnMf3AjZ"
mapping = define_mapping(inputs = ['X', 'Y', 'Z'], outputs = [0, 1, 2])

# + [markdown] id="DORsrxK93Ajb"
# **Task 2**: Set `inputs` and `outputs` to create another mapping, this time from values `0, 1, 2` to characters `X, Y, Z`.

# + id="4Xxe5wo13Ajc"
inverse_mapping = define_mapping(inputs = [0, 1, 2], outputs = ['X', 'Y', 'Z'])

# + [markdown] id="LIRnRJkB3Ajd"
# **Task 3**: What happens if we call `inverse_mapping` after `mapping` on the characters `X`, `Y`, or `Z`? 

# + id="8CvZTiif3Aje"
print(inverse_mapping(mapping('X')))
print(inverse_mapping(mapping('Y')))
print(inverse_mapping(mapping('Z')))


# + [markdown] id="mmTHO_2-3Aje"
# **Task 4**: Define a mapping which does *not* have an inverse mapping.

# + id="5g33Zria3Ajf"
no_inverse_mapping = define_mapping(inputs = [0, 1], outputs = ['X', 'X'])


# + [markdown] id="q7siTWHk3Ajg"
# ## Encoding

# + [markdown] id="i5paTnb83Ajg"
# A character encoding is just a mapping from characters to numerical values (integers or bytes).

# + [markdown] id="qB0xD_Uf3Ajh"
# **Task 1**: Check whether a given string `s` can be encoded using the ASCII encoding. You can use the `encode` method [str.encode()](https://docs.python.org/3/library/stdtypes.html#str.encode/) from the Python standard library .

# + id="JlSgBxg73Ajj"
s = 'AB\tC\t\t'
s.encode('ASCII')

# + [markdown] id="TeHAqPuO3Ajk"
# **Task 2**: Find a character that cannot be encoded using ASCII. Check whether it can be encoded using the UTF-8 encoding.

# + id="UIYzx6tk3Ajl"
try:
    "ž".encode('ASCII')
except UnicodeEncodeError:
    print("Cannot encode")

"ž".encode('UTF-8')


# + [markdown] id="0nkOx1Lt3Ajv"
# **Task 3**: Replace zeros (and nothing else) in the following expression such that the output is `b'ABC ABC ABC ABC '`.

# + id="4pBynj8U3Ajw" outputId="f5c4471f-7af3-48c7-e24f-30950c2cfb7e"
print(b'ABC ' + bytes([65,66,67,32]) + bytes.fromhex('41424320') + b'\x41\x42\x43\x20')

# + [markdown] id="Qr4panus3Ajx"
# **Task 4**: Look into the ASCII table and replace the integers in the definition of `alphabet_bytes` to obtain the alphabet `a-zA-Z0-9`.

# + id="I_dsiVV93Ajx" outputId="90740d54-a051-4aaa-dd63-6bf517dab1f9"
alphabet_bytes = bytes(range(97,123)) + bytes(range(65,91)) + bytes(range(48,58))
print(alphabet_bytes.decode('ASCII'))
print(alphabet_bytes.decode('ASCII') == 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') # verification

# + [markdown] id="8W_gNRu63Ajy"
# **Task 5**: Use `define_mapping` to create an encoding function `encode_char` that encodes the alphabet `a-zA-Z0-9` as integers `0-61`.

# + id="jK-mL90a3Ajz"
alphabet = alphabet_bytes.decode('ascii')
encode_char = define_mapping(alphabet, range(62))
encode_char('a')

# + [markdown] id="gwZzJ6hg3Aj0"
# Test your solution below.

# + id="gseAiO3g3Aj1" outputId="d1539772-f46e-4080-e4a4-6011c037c546"
print(encode_char('a') == 0)
print(encode_char('Z') == 51)
print(encode_char('9') == 61)

# + [markdown] id="1_EybZ4h3Aj1"
# Being able to encode just a single character is impractical. The following function encodes a text input of *arbitrary* length.

# + id="4XgCjSvW3Aj2"
import string

def encode_text(text):
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + ' .'
    char_codes = list(range(len(alphabet)))
    encoder = define_mapping(alphabet, char_codes)
    return [encoder(character) for character in list(text)]


# + [markdown] id="qNEaP40H3Aj3"
# **Task 6**: Implement `decode_text`, a decoding function which corresponds to `encode_text`.

# + id="tTityyXM3Aj3"
def decode_text(codes):
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + ' .'
    char_codes = list(range(len(alphabet)))
    decoder = define_mapping(char_codes, alphabet)
    return [decoder(character_code) for character_code in codes] # map(decoder, text)


# + [markdown] id="GngeFutO3Aj3"
# Test your solution.

# + id="iwfPLD0Z3Aj4"
msg = 'Hello world'
decode_text(encode_text(msg))

# + [markdown] id="_0urX9k73Aj4"
# **Task 7**: Change the order - decode some text first, then encode it. Does it work? Why?

# + id="WKkA8iDY3Aj5"
try:
    encode_text(decode_text(msg))
except KeyError:
    print("Cannot map some character.")


# + [markdown] id="v7Lr5CjS3Aj5"
# ## Stream ciphers

# + [markdown] id="shtgN_2F3Aj6"
# Once we know how a particular mapping works, it's easy to construct the reverse mapping. To be able to **encrypt**, we will need an additional parameter, the **key**.

# + [markdown] id="yKHEuf4M3Aj6"
# ### Basic Caesar-like cipher
#
# A cipher is a set of different mappings each defined by a different key.

# + [markdown] id="7B87ZD8V3Aj7"
# The function `secret_mapping` returns different mappings of the alphabet for different keys (in this case integers).

# + id="vS9zwS9p3Aj8"
def secret_mapping(key):
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + ' .'
    char_codes = list(range(len(alphabet)))
    rotated_codes = char_codes[key:] + char_codes[:key]
    return define_mapping(alphabet, rotated_codes)


# + [markdown] id="vtUOJtfY3Aj9"
# **Task 1**: Implement `secret_inverse_mapping` correspoding to `secret_mapping` above. 

# + id="7ok9q2Ee3Aj9"
def secret_inverse_mapping(key):
    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + ' .'
    char_codes = list(range(len(alphabet)))
    rotated_codes = char_codes[key:] + char_codes[:key]
    return  define_mapping(rotated_codes, alphabet)


# -

# Test the correctness of your solution. Map the characters `a`, `B`, `1` using the `secret_mapping` with key `1` and then map them back using `secret_inverse_mapping`.

key = 1
encryption_mapping = secret_mapping(key)
decryption_mapping = secret_inverse_mapping(key)
encrypted_character = encryption_mapping('a')
print(decryption_mapping(encrypted_character))


# + [markdown] id="Ugjjwyy83Aj-"
# The function `basic_encrypt` encrypts a given `plaintext` of arbitrary length using a secret mapping with key `key`.

# + id="dLTfBhYm3Aj-"
def basic_encrypt(plaintext: str, key: int) -> list[int]:
    encryption_mapping = secret_mapping(key)
    return [encryption_mapping(character) for character in list(plaintext)] # map(encryption_mapping, plaintext)


# -

# **Task 2**: Implement a decryption function `basic_decrypt` corresponding to the encryption function `basic_encrypt`.

def basic_decrypt(ciphertext: list[int], key: int) -> str:
    decryption_mapping = secret_inverse_mapping(key)
    return ''.join([decryption_mapping(value) for value in ciphertext])


# Decrypt `ct` and check the result. Is it equal to `msg`?

msg = 'Arbitrary message but from given alphabet'
ct = basic_encrypt(msg, 3)
print(basic_decrypt(ct, 3))

# + [markdown] id="0zaIFEYW3Aj_"
# ### Statistical analysis
# When the plaintext contains two identical letters, `basic_encrypt` maps them to identical values in the ciphertext. 
#
# In English, letters are not typically used evenly. Knowing this, we can try to deduce the key from the frequencies of values in the ciphertext.
# -

# See how `Counter` is used to compute the frequencies of elements in a list.

import string
from collections import Counter
print(Counter([1,1,2,2,2]))

# + [markdown] id="fwSTy4kb3Aj_"
# **Task 1**: Use `Counter` to compute frequencies of letters in `msg`.

# + id="nVkkmrv03Aj_" outputId="91396ecf-ed8b-41e9-ff62-07c516b97c00"
msg = "The Bible is a collection of religious texts or scriptures that are held to be sacred in Christianity, Judaism, Samaritanism, and many other religions."
print(Counter(msg))

# + [markdown] id="5KeKg4y23AkA"
# **Task 2**: Encrypt alphabet using `basic_encrypt` with different keys (`K = 0`, `K = 1`, `K = 2`).

# + id="6yccR0yR3AkA"
alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + ' .'
print(basic_encrypt(alphabet, 0))
print(basic_encrypt(alphabet, 1))
print(basic_encrypt(alphabet, 2))

# + [markdown] id="n7Rx_tm83AkB"
# **Task 3**: Compute the frequencies of values in the ciphertext `ct` (obtained using `basic_encrypt`), find the right key and decrypt the ciphertext.

# + id="oi-tpt1f3AkB"
ct = [39, 32, 11, 32, 20, 17, 11, 18, 21, 30, 31, 32, 11, 45, 27, 16, 11, 25, 13, 16, 17, 11, 32, 20, 17, 11, 20, 17, 13, 34, 17, 26, 11, 13, 26, 16, 11, 32, 20, 17, 11, 17, 13, 30, 32, 20, 12, 11, 39, 26, 16, 11, 32, 20, 17, 11, 17, 13, 30, 32, 20, 11, 35, 13, 31, 11, 35, 13, 31, 32, 17, 11, 13, 26, 16, 11, 35, 21, 32, 20, 27, 33, 32, 11, 18, 27, 30, 25, 11, 13, 26, 16, 11, 21, 32, 11, 35, 13, 31, 11, 16, 13, 30, 23, 11, 27, 26, 11, 32, 20, 17, 11, 18, 13, 15, 17, 11, 27, 18, 11, 32, 20, 17, 11, 16, 17, 17, 28, 11, 13, 26, 16, 11, 32, 20, 17, 11, 57, 28, 21, 30, 21, 32, 11, 27, 18, 11, 45, 27, 16, 11, 35, 13, 31, 11, 25, 27, 34, 21, 26, 19, 11, 27, 26, 11, 32, 20, 17, 11, 18, 13, 15, 17, 11, 27, 18, 11, 32, 20, 17, 11, 35, 13, 32, 17, 30, 31, 12]

# Space is the most common character in English text
space_pos = alphabet.find(' ')
# Find the most common value in the ciphertext, this is the encrypted space
most_common_ct_value = Counter(ct).most_common()[0][0]
# The key is the difference between the most common value and the position of the space in the alphabet
key = (most_common_ct_value - space_pos) % len(alphabet)

basic_decrypt(ct, key)


# + [markdown] id="evjrhTc_3AkC"
# ### Vernam cipher
# So far, we have been encrypting text messages. However, it is usually more convenient to work with binary messages directly. In Python, we will use the `bytes` type for that.
#

# + [markdown] id="lQKjngw-3AkC"
# **Task 1**: What is the result of bitwise XOR: $11000111_2 \oplus 11010010_2$?
#
# Set the two variables `a`, `b` accordingly and compare your answer to the question with `c`. Beware, `bytes.fromhex()` expects a hexadecimal number.

# + id="NSmiUKOh3AkD" outputId="30811287-e553-4fd2-bb3b-937e729cbbe4"
def XOR(array1: bytes, array2: bytes) -> bytes:
    l = min(len(array1), len(array2))
    xored = bytes(a ^ b for (a, b) in zip(array1, array2))
    if len(array1) > l:
        xored += array1[l:]
    else:
        xored += array2[l:]
    return xored

a = bytes.fromhex('c7')
b = bytes.fromhex('d2')
c = XOR(a, b)
c.hex()

# + [markdown] id="0dloUDUE3AkD"
# **Task 2**: Using `c` and `a` compute `b_computed` and compare with the original `b`. Use the `XOR` function and the fact $c = a \oplus b$.

# + id="n2oa_zNJ3AkD" outputId="cba3f297-c878-47dd-8b45-5aa4c4cf2203"
b_computed = XOR(c, a)
print(b_computed == b) #verification
# -

# To generate random binary data (e.g. keys), we will be using the `secrets` library. 

# +
import secrets

key = secrets.token_bytes(32)
print(key)


# + [markdown] id="DiL_5XLt3AkE"
# **Task 3**: Fix the returned value of the `Vernam` function.

# + id="0PlYs0Ms3AkE" outputId="0f802a2c-5979-4bb4-fcd4-b2caf774c423"
def Vernam(text: bytes, key: bytes) -> bytes:
    assert len(text) <= len(key), f'The key is shorter than the encrypted/decrypted text.'
    return XOR(text, key)


# -

# Check that the decrypted plaintext corresponds to the original message.

msg = b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
key = secrets.token_bytes(len(msg))
ct = Vernam(msg, key)
pt = Vernam(ct, key)
print(pt)

# + [markdown] id="WACofkHM3AkG"
# ### Chacha20
# Modern stream ciphers like Chacha20 encrypt plaintext by XORing it with a "keystream" generated from a key and a nonce (random bitstring). Importantly, the key is of fixed size, usually much shorter than the plaintext.

# + id="oTG9MmSd3AkH"
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

def chacha20_encrypt(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    algorithm = algorithms.ChaCha20(key, nonce)
    encryptor = Cipher(algorithm, mode=None).encryptor()
    ct = encryptor.update(plaintext) + encryptor.finalize()
    return ct

def chacha20_decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    algorithm = algorithms.ChaCha20(key, nonce)
    decryptor = Cipher(algorithm, mode=None).decryptor()
    pt = decryptor.update(ciphertext) + decryptor.finalize()
    return pt

msg = b'Far far away, behind the word mountains, far from the countries.'

# + [markdown] id="y4k7Z5Aw3AkI"
# **Task 1**: Replace zeros with correct key/nonce sizes to encrypt the message `msg` using Chacha20. See [chacha20 documentation](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.algorithms.ChaCha20).

# + id="x6n8oV3_3AkI" outputId="0bc8a5e9-db14-43c3-aaa0-7744b1553f68"
key = secrets.token_bytes(32)
nonce = secrets.token_bytes(16)
ct = chacha20_encrypt(msg, key, nonce)
pt = chacha20_decrypt(ct, key, nonce)

# + [markdown] id="EJCvmGQT3AkJ"
# **Task 2**: Change the plaintext `pt` so that by encrypting it, you obtain the first 64 bytes of the keystream. Remember how the ciphertext is computed from the plaintext and the keystream.

# + id="xX8ck3xf3AkJ" outputId="963d19d4-ab4b-4349-cea9-5ccaf33409ea"
pt = bytes.fromhex('00'*64)
keystream = chacha20_encrypt(pt, key, nonce)
print(keystream)


# + [markdown] id="2fJp0rrv3AkK"
# Verify that the ciphertext `ct` can be obtained directly as a XOR of `msg` and `keystream`.

# + id="W3sL4UW33AkK" outputId="e030763b-a898-4d10-e04d-b8a801676c4a"
ct2 = XOR(msg, keystream)
ct2 == ct

# + [markdown] id="88nEqYBX3AkL"
# **Task 3**: Use two nonces which differ in single bit and compare corresponding keystreams. How much do they differ?

# + id="cwW86zeJ3AkL" outputId="47c89254-c597-4bfe-d962-32f10890cd24"
pt = bytes.fromhex('00'*10)
nonce1 = bytes.fromhex('00'*16)
nonce2 = bytes.fromhex('00'*15 + '01')
keystream1 = chacha20_encrypt(pt, key, nonce1)
keystream2 = chacha20_encrypt(pt, key, nonce2)
print(keystream1)
print(keystream2)
