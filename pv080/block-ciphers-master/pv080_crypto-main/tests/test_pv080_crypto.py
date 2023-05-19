import secrets
import random

from pv080_crypto.symmetric import pad, unpad
from pv080_crypto.symmetric import aes_encrypt, aes_decrypt
from pv080_crypto.symmetric import aes_ecb_encrypt, aes_ecb_decrypt
from pv080_crypto.symmetric import aes_cbc_encrypt, aes_cbc_decrypt
from pv080_crypto.symmetric import create_mac, verify_mac
from pv080_crypto.asymmetric import rsa_encrypt, rsa_decrypt
from pv080_crypto.asymmetric import create_signature, verify_signature
from cryptography.hazmat.primitives.asymmetric import rsa

import pytest
from hypothesis import given
from hypothesis.strategies import binary


@given(data=binary())
def test_pad_pads_to_multiple_of_sixteen(data):
    assert len(pad(data=data, block_size=128)) % 16 == 0


@given(data=binary())
def test_pad_unpad_roundtrip(data):
    assert unpad(pad(data, block_size=16), block_size=16) == data


@given(
    iv=binary(min_size=16, max_size=16),
    key=binary(min_size=16, max_size=32).filter(lambda x: len(x) in [16, 24, 32]),
    data=binary(),
)
def test_aes_ecb_encrypt_decrypt_roundtrip(iv, key, data):
    padded_msg = pad(data, block_size=128)
    ciphertext = aes_ecb_encrypt(key=key, padded_plaintext=padded_msg)
    padded_plaintext = aes_ecb_decrypt(key=key, ciphertext=ciphertext)
    plaintext = unpad(padded_plaintext, block_size=128)
    assert plaintext == data


@given(
    iv=binary(min_size=16, max_size=16),
    key=binary(min_size=16, max_size=32).filter(lambda x: len(x) in [16, 24, 32]),
    data=binary(),
)
def test_aes_cbc_encrypt_decrypt_roundtrip(iv, key, data):
    padded_msg = pad(data, block_size=128)
    ciphertext = aes_cbc_encrypt(key=key, iv=iv, padded_plaintext=padded_msg)
    padded_plaintext = aes_cbc_decrypt(key=key, iv=iv, ciphertext=ciphertext)
    plaintext = unpad(padded_plaintext, block_size=128)
    assert plaintext == data


@pytest.mark.parametrize("key_size", [16, 24, 32])
def test_aes_encrypt_decrypt_roundtrip(key_size: int):
    for _ in range(10):
        # generate a random message of random length
        message_length = random.randint(0, 2**16)
        message = secrets.token_bytes(message_length)

        key = secrets.token_bytes(key_size)
        # test encrypt/decrypt roundtrip
        ciphertext = aes_encrypt(key=key, message=message)
        plaintext = aes_decrypt(key=key, ciphertext=ciphertext)
        assert message == plaintext


@pytest.mark.parametrize(
    "public_exponent,key_size",
    [
        (3, 1024),
        (3, 2048),
        (65537, 1024),
        (65537, 2048),
    ],
)
def test_rsa_encrypt_decrypt_roundtrip(public_exponent: int, key_size: int):
    for _ in range(10):
        # generate a random message shorter than the key size
        message = secrets.token_bytes(key_size // 32)

        privkey = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size,
        )
        pubkey = privkey.public_key()

        ciphertext = rsa_encrypt(key=pubkey, plaintext=message)
        plaintext = rsa_decrypt(key=privkey, ciphertext=ciphertext)

        assert message == plaintext


@pytest.mark.parametrize("key_size", [16, 24, 32])
def test_mac_verification(key_size: int):
    for _ in range(10):
        key = secrets.token_bytes(key_size)
        length = random.randint(0, 2**16)
        data = secrets.token_bytes(length)

        mac = create_mac(key=key, data=data)
        assert verify_mac(key=key, data=data, mac=mac)


@pytest.mark.parametrize(
    "public_exponent,key_size",
    [
        (3, 1024),
        (3, 2048),
        (65537, 1024),
        (65537, 2048),
    ],
)
def test_digital_signatures(public_exponent: int, key_size: int):
    for _ in range(10):
        length = random.randint(0, 2**16)
        data = secrets.token_bytes(length)

        privkey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        pubkey = privkey.public_key()

        signature = create_signature(private_key=privkey, data=data)
        assert verify_signature(public_key=pubkey, data=data, signature=signature)
