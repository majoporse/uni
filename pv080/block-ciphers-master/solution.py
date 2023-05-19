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

# # Seminar 04: Block Ciphers, Server Communication

# In the remaining cryptography seminars, you will use mainly functions from the `pv080_crypto` library. Its documentation is available on the [course webpage](https://pv080.fi.muni.cz/docs/).
#
# Run the following cell to import the functions needed today.

import secrets
from pv080_crypto import XOR, pad, unpad
from pv080_crypto import aes_ecb_encrypt, aes_ecb_decrypt, aes_cbc_encrypt, aes_cbc_decrypt
from pv080_crypto import send_message, recv_message

# ## 1. AES and padding

#   **Task 1.1**: Use [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt) to encrypt the message `msg`. See the function documentation for appropriate key size.

msg = b'when Gregor Samsa woke from troubled dreams, he found himself transformed into a horrible vermin'
key = secrets.token_bytes(16)
aes_ecb_encrypt(key, msg)

# **Task 1.2**: Execute the following cell. Why does the encryption fail? Fix the issue using the padding function [`pad`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.pad).

msg = pad(b'I like crypto.', 128)
aes_ecb_encrypt(key, msg)

#  **Task 1.3**: Apply [`pad`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.pad) to data of various lengths and figure out how the padding (PKCS7) works.

for i in range(20):
    pt = bytes.fromhex('00'*i)
    print(list(pad(pt, 128)))

#  **Task 1.4**: Identify the length of the padding after decrypting `ct` and remove it without using the `unpad` function (change 0 in the list slicing appropriately). Verify your solution by padding the obtained plaintext and re-encrypting it.

key = bytes.fromhex('00' * 16)
ct = b'\xc4\xb6\xa6\x01\x10C8F\x8e\xc0\x87e\xe7\x03\xff\x9f'
pt = aes_ecb_decrypt(key, ct)[:-5]
ct == aes_ecb_encrypt(key, pad(pt,128))

#  **Task 1.5**: Encrypt and decrypt the message `msg`. Use only [`pad`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.pad), [`unpad`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.unpad), [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt), and [`aes_ecb_decrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_decrypt).

msg = "My super secret message to be encrypted."
key = secrets.token_bytes(16)
padded_msg = pad(msg.encode(), 128)
ct = aes_ecb_encrypt(key, padded_msg)
padded_pt = aes_ecb_decrypt(key, ct)
pt = unpad(padded_pt, 128)
print(pt.decode()==msg)

# ## 2. Block cipher modes of operation

# **Task 2.1**: Encrypt 3 blocks of zero bytes using [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt) and examine the ciphertext. Do you see a pattern? How often does it repeat?

key = secrets.token_bytes(24)
msg = bytes.fromhex('00'*16*3)
aes_ecb_encrypt(key, msg).hex()

# **Task 2.2**: Encrypt `msg` using [`aes_cbc_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_cbc_encrypt). Then flip a single bit of `iv` and see how the ciphertext changes.

msg = pad(b'Twas brillig, and the slithy toves did gyre and gimble in the wabe', 128)
key = secrets.token_bytes(32)
iv = bytes.fromhex('11'*16)
ct = aes_cbc_encrypt(key, iv, msg)
print(ct.hex())
iv = bytes.fromhex('11'*15 + '10')
aes_cbc_encrypt(key, iv, msg).hex()

# ## 3. Server communication: Introduction

# To communicate over server, you can use the functions [`send_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.send_message) and [`recv_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.recv_message). The two functions use UČOs to identify the sender and the receiver. The server always stores **only the most recent message** from a given sender to a given receiver.

# **Task 3.1**: Use [`send_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.send_message) to send an arbitrary message to yourself. Repeat this a few times with different messages.

uco = 232886
send_message(uco, uco, b'test msg2')

# **Task 3.2**: Use [`recv_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.recv_message) to download the dictionary of messages sent to you. Print out the message (not the whole dictionary) that you sent to yourself.

msg_dict = recv_message(uco)
print(msg_dict[uco])

# ## 4. Server communication: Pair activity

#
# Form a pair with your classmate and work on the following tasks together.

# **Task 4.1**: Send an unencrypted message to your partner, wait until they answer and obtain the answer from the server.

my_uco = 232886
partners_uco = 232886
send_message(my_uco, partners_uco, b'Hi Marek')

# **Task 4.2**: Repeat the previous task but encrypt the message using [`aes_cbc_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_cbc_encrypt) with zero key (key formed of zero bytes). Agree on the format of the transmitted data with your partner - you must send a random `iv` together with the message.

# +
key = bytes.fromhex('00'*16)
msg = b'Hi Marek'
padded_msg = pad(msg, 128)
iv = bytes.fromhex('00'*16)
ct = aes_cbc_encrypt(key, iv, padded_msg)

send_message(my_uco, partners_uco, iv+ct)
# -

# Receive the message from your partner and decrypt it. Be careful to correctly split the received message into ciphertext and IV (based on the agreement with your partner).

payload = recv_message(my_uco)[partners_uco]
iv, ct = payload[:16], payload[16:]
padded_pt = aes_cbc_decrypt(key, iv, ct)
unpad(padded_pt, 128)

# **Task 4.3**: Generate a random key and exchange it with your partner using pen and paper. **Only one of you generates the key!**

# +
import secrets

# Generate the key and print it in hex to exchange it.
key = secrets.token_bytes(16)
print(key.hex())

# Load the key from a hex string as written on the paper.
key = bytes.fromhex('00112233445566778899aabbccddeeff')


# -

# **Task 4.4**: Encrypt a message for your partner using the exchanged key.

# +
# Same as before
# -

# Receive the message from your partner and decrypt it.

# +
# Same as before
# -

# **Task 4.5**: Continue in the communication and exchange more encrypted messages - use the same key. Secure communication should use a unique IV for each message!

# +
# Same as before
# -

# ## 5. Bonus Tasks

# **Task 5.1**: Implement `my_aes_cbc_encrypt` and `my_aes_cbc_decrypt` using only the functions [`XOR`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.XOR), [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt), and [`aes_ecb_decrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_decrypt). See the slides for encryption schemes.

# +
def my_aes_cbc_encrypt(key: bytes, iv: bytes, padded_plaintext: bytes) -> bytes:
    ct = b''
    while padded_plaintext:
        ct_block = aes_ecb_encrypt(key, XOR(iv, padded_plaintext[:16]))
        ct += ct_block
        iv = ct_block
        padded_plaintext = padded_plaintext[16:]
    return ct

def my_aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    ecb_decrypted_ct = aes_ecb_decrypt(key, ciphertext)
    xor_stream = iv + ciphertext[:-16]
    return XOR(ecb_decrypted_ct, xor_stream)


# -

# Verify that the functions work identically to [`aes_cbc_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_cbc_encrypt) and [`aes_cbc_decrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_cbc_decrypt).

key = secrets.token_bytes(16)
iv = secrets.token_bytes(16)
pt = secrets.token_bytes(3 * 16)
ct = aes_cbc_encrypt(key, iv, pt)
my_ct = my_aes_cbc_encrypt(key, iv, pt)
assert ct == my_ct
decrypted = aes_cbc_decrypt(key, iv, ct)
my_decrypted = my_aes_cbc_decrypt(key, iv, ct)
assert decrypted == my_decrypted


# **Task 5.2:** Implement `my_aes_ctr_encrypt` and `my_aes_ctr_decrypt` using only [`XOR`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.XOR), [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt), and [`aes_ecb_decrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_decrypt). To  construct the counter stream, use a 128-bit nonce and increment it with each block.

# +
def counter(blocks, nonce):
    def increment(data: bytes, add: int) -> bytes:
        return (int.from_bytes(data, 'big') + add).to_bytes(16, 'big')
    return b''.join([increment(nonce, i) for i in range(blocks)])

def my_aes_ctr_encrypt(key: bytes, nonce: bytes, padded_plaintext: bytes) -> bytes:
    ctr = counter(len(padded_plaintext) // 16, nonce)
    encrypted_ctr = aes_ecb_encrypt(key, ctr)
    return XOR(encrypted_ctr, padded_plaintext)

def my_aes_ctr_decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    ctr = counter(len(ciphertext) // 16, nonce)
    encrypted_ctr = aes_ecb_encrypt(key, ctr)
    return XOR(encrypted_ctr, ciphertext)


# -

# **Task 5.3** Implement `aes_ctr_encrypt` and `aes_ctr_decrypt` using the `cryptography` library. Use its [documentation](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#).

# +
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def aes_ctr_encrypt(key: bytes, nonce: bytes, padded_plaintext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ct

def aes_ctr_decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    padded_pt = decryptor.update(ciphertext)
    return padded_pt


# -

# Verify that `aes_ctr_encrypt` and `my_aes_ctr_encrypt` (and the decryption functions) work identically.

key = secrets.token_bytes(16)
nonce = secrets.token_bytes(16)
pt = secrets.token_bytes(32)
my_ct = my_aes_ctr_encrypt(key, nonce, pt)
ct = aes_ctr_encrypt(key, nonce, pt)
assert my_ct == ct
decrypted = aes_ctr_decrypt(key, nonce, ct)
my_decrypted = my_aes_ctr_decrypt(key, nonce, ct)
assert decrypted == my_decrypted
