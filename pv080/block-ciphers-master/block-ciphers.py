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
# from pv080_crypto import XOR, pad, unpad
from pv080_crypto import aes_ecb_encrypt, aes_ecb_decrypt, aes_cbc_encrypt, aes_cbc_decrypt
# from pv080_crypto import send_message, recv_message

# ## 1. AES and padding

#   **Task 1.1**: Use [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt) to encrypt the message `msg`. See the function documentation for appropriate key size.

import secrets
msg = b'when Gregor Samsa woke from troubled dreams, he found himself transformed into a horrible vermin'
key = secrets.token_bytes(0)
pmsg = pad(msg, 128)
cmsg = aes_ecb_encrypt(key, pmsg)

# **Task 1.2**: Execute the following cell. Why does the encryption fail? Fix the issue using the padding function [`pad`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.pad).

msg = b'I like crypto.'
pmsg = pad(msg)
aes_ecb_encrypt(key, pmsg)

#  **Task 1.3**: Apply [`pad`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.pad) to data of various lengths and figure out how the padding (PKCS7) works.

for i in range(20):
    data = bytes.fromhex('00'*i)
    print(data) # Apply padding to `data`

#  **Task 1.4**: Identify the length of the padding after decrypting `ct` and remove it without using the `unpad` function (change 0 in the list slicing appropriately). Verify your solution by padding the obtained plaintext and re-encrypting it.

key = bytes.fromhex('00' * 16)
ct = b'\xc4\xb6\xa6\x01\x10C8F\x8e\xc0\x87e\xe7\x03\xff\x9f'
pt = aes_ecb_decrypt(key, ct)[:0]
upt = unpad(pt) # Slice the plaintext appropriately

#  **Task 1.5**: Encrypt and decrypt the message `msg`. Use only [`pad`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.pad), [`unpad`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.unpad), [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt), and [`aes_ecb_decrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_decrypt).

msg = b"My super secret message to be encrypted."
key = secrets.token_bytes(16)
pm = pad(msg)
ct = aes_ecb_encrypt(pm, 128)
uct = aes_ecb_decrypt(ct, 128)
upm = unpad(uct)


# ## 2. Block cipher modes of operation

# **Task 2.1**: Encrypt 3 blocks of zero bytes using [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt) and examine the ciphertext. Do you see a pattern? How often does it repeat?

a = aes_scb_encrypt('00'*3, 16)

# **Task 2.2**: Encrypt `msg` using [`aes_cbc_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_cbc_encrypt). Then flip a single bit of `iv` and see how the ciphertext changes.

msg = pad(b'Twas brillig, and the slithy toves did gyre and gimble in the wabe', 128)
key = secrets.token_bytes(32)
iv = bytes.fromhex('11'*16)
cm = aes_cbc_encrypt()

# ## 3. Server communication: Introduction

# To communicate over server, you can use the functions [`send_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.send_message) and [`recv_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.recv_message). The two functions use UČOs to identify the sender and the receiver. The server always stores **only the most recent message** from a given sender to a given receiver.

# **Task 3.1**: Use [`send_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.send_message) to send an arbitrary message to yourself. Repeat this a few times with different messages.



# **Task 3.2**: Use [`recv_message`](https://pv080.fi.muni.cz/docs/api/messaging.html#pv080_crypto.messaging.recv_message) to download the dictionary of messages sent to you. Print out the message (not the whole dictionary) that you sent to yourself.



# ## 4. Server communication: Pair activity

#
# Form a pair with your classmate and work on the following tasks together.

# **Task 4.1**: Send an unencrypted message to your partner, wait until they answer and obtain the answer from the server.



# **Task 4.2**: Repeat the previous task but encrypt the message using [`aes_cbc_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_cbc_encrypt) with zero key (key formed of zero bytes). Agree on the format of the transmitted data with your partner - you must send a random `iv` together with the message.

key = bytes.fromhex('00'*16)
iv = secrets.token_bytes(16)

# Receive the message from your partner and decrypt it. Be careful to correctly split the received message into ciphertext and IV (based on the agreement with your partner).



# **Task 4.3**: Generate a random key and exchange it with your partner using pen and paper. **Only one of you generates the key!**



# **Task 4.4**: Encrypt a message for your partner using the exchanged key.



# Receive the message from your partner and decrypt it.



# **Task 4.5**: Continue in the communication and exchange more encrypted messages - use the same key. Secure communication should use a unique IV for each message!



# ## 5. Bonus Tasks

# **Task 5.1**: Implement `my_aes_cbc_encrypt` and `my_aes_cbc_decrypt` using only the functions [`XOR`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.XOR), [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt), and [`aes_ecb_decrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_decrypt). See the slides for encryption schemes.

# +
def my_aes_cbc_encrypt(key: bytes, iv: bytes, padded_plaintext: bytes) -> bytes:
    pass


def my_aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    pass
# -

# Verify that the functions work identically to [`aes_cbc_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_cbc_encrypt) and [`aes_cbc_decrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_cbc_decrypt).



# **Task 5.2:** Implement `my_aes_ctr_encrypt` and `my_aes_ctr_decrypt` using only [`XOR`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.XOR), [`aes_ecb_encrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_encrypt), and [`aes_ecb_decrypt`](https://pv080.fi.muni.cz/docs/api/symmetric.html#pv080_crypto.symmetric.aes_ecb_decrypt). To construct the counter stream, use a 128-bit nonce and increment it with each block.

# +
def my_aes_ctr_encrypt(key: bytes, nonce: bytes, padded_plaintext: bytes) -> bytes:
    pass


def my_aes_ctr_decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    pass


# -

# **Task 5.3** Implement `aes_ctr_encrypt` and `aes_ctr_decrypt` using the `cryptography` library. Use its [documentation](https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#).

# +
def aes_ctr_encrypt(key: bytes, nonce: bytes, padded_plaintext: bytes) -> bytes:
    pass


def aes_ctr_decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    pass
# -

# Verify that `aes_ctr_encrypt` and `my_aes_ctr_encrypt` (and the decryption functions) work identically.


