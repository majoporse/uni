"""The :py:mod:`symmetric <pv080_crypto.symmetric>` module provides the
function to perform encryption and decryption operation and also MACs.
Naturally, the functions with the suffix ``_encrypt`` are for encryption and
``_decrypt`` for decryption. The underlying block cipher used is `Advanced
Encryption Standard <https://wikipedia.org/wiki/Advanced_Encryption_Standard>`_
(AES).

There are also lower level primitives such as :py:func:`XOR
<pv080_crypto.symmetric.XOR>`, :py:func:`pad <pv080_crypto.symmetric.pad>` and
:py:func:`unpad <pv080_crypto.symmetric.unpad>`.

Finally, there are functions :py:func:`create_mac
<pv080_crypto.symmetric.create_mac>` and :py:func:`verify_mac
<pv080_crypto.symmetric.verify_mac>` for creating and verifying `Message
Authentication Codes
<https://en.wikipedia.org/wiki/Message_authentication_code>`_ (MACs). """

#!/usr/bin/env python3
import hashlib
import requests
import secrets

from binascii import hexlify, unhexlify
from typing import Mapping, Union, Optional, Tuple

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as padding_symmetric
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import padding as padding_asymmetric
from cryptography.hazmat.primitives import hashes

# FIXME: the documentation could use some polishing. Improve readbility, consistency
#        and English.
# FIXME: format the code including the docs to fit into 80 columns


def pad(data: bytes, block_size: int) -> bytes:
    """
    Appends PKCS7 padding to ``data`` so that its size is a multiple of ``block_size``.

    :param data: The unpadded data which we want to pad.
    :param block_size: The block size in bits, usually given by the cipher that we want to use.

    :returns: The padded data.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(16)
    >>> pt = b'message'
    >>> padded_pt = pad(pt, 128)
    >>> ct = aes_ecb_encrypt(key, padded_pt)
    """
    padder = padding_symmetric.PKCS7(block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


def unpad(padded_data: bytes, block_size: int) -> bytes:
    """
    Removes PKCS7 padding from ``padded_data``.

    :param padded_data: The padded data which we want to unpad.
    :param block_size: The block size in bits, usually given by the cipher that we want to use.

    :returns: The unpadded data.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(16)
    >>> pt = b'message'
    >>> padded_pt = pad(pt, 128)
    >>> ct = aes_ecb_encrypt(key, padded_pt)
    >>> decrypted = aes_ecb_decrypt(key, ct)
    >>> assert unpad(decrypted, 128) == pt
    """
    unpadder = padding_symmetric.PKCS7(block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data


def aes_ecb_encrypt(key: bytes, padded_plaintext: bytes) -> bytes:
    """
    Encrypts ``padded_plaintext`` with ``key`` using AES-ECB.

    :param key: The encryption key of size 128, 192, or 256 bits.
    :param padded_plaintext: The bytes to be encrypted (must be padded to 128 bits).

    :returns: The bytes of the encrypted ciphertext.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(16)
    >>> pt = b'message'
    >>> padded_pt = pad(pt, 128)
    >>> ct = aes_ecb_encrypt(key, padded_pt)
    """
    cipher = Cipher(algorithms.AES(key), mode=modes.ECB())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ct


def aes_ecb_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypts ``ciphertext`` with ``key`` using AES-ECB.

    :param key: The encryption key of size 128, 192, or 256 bits.
    :param ciphertext: The bytes to be decrypted.

    :returns: The bytes of the padded plaintext.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(16)
    >>> pt = b'message'
    >>> padded_pt = pad(pt, 128)
    >>> ct = aes_ecb_encrypt(key, padded_pt)
    >>> decrypted = aes_ecb_decrypt(key, ct)
    >>> assert unpad(decrypted, 128) == pt
    """
    cipher = Cipher(algorithms.AES(key), mode=modes.ECB())
    decryptor = cipher.decryptor()
    padded_pt = decryptor.update(ciphertext)
    return padded_pt


def aes_cbc_encrypt(key: bytes, iv: bytes, padded_plaintext: bytes) -> bytes:
    """
    Encrypts ``padded_plaintext`` with ``key`` using AES-CBC and ``iv``.

    :param key: The encryption key of size 128, 192, or 256 bits.
    :param iv: The initialization vector (must be of size 128 bits).
    :param padded_plaintext: The bytes to be encrypted (must be padded to 128 bits).

    :returns: The bytes of the encrypted ciphertext.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(16)
    >>> iv = secrets.token_bytes(16)
    >>> pt = b'message'
    >>> padded_pt = pad(pt, 128)
    >>> ct = aes_cbc_encrypt(key, iv, padded_pt)
    """
    cipher = Cipher(algorithms.AES(key), mode=modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_plaintext) + encryptor.finalize()
    return ct


def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    """
    Decrypts ``ciphertext`` with ``key`` using AES-CBC and ``iv``.

    :param key: The encryption key of size 128, 192, or 256 bits.
    :param iv: The initialization vector (must be of size 128 bits).
    :param ciphertext: The bytes to be decrypted.

    :returns: The bytes of the padded plaintext.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(16)
    >>> iv = secrets.token_bytes(16)
    >>> pt = b'message'
    >>> padded_pt = pad(pt, 128)
    >>> ct = aes_cbc_encrypt(key, iv, padded_pt)
    >>> decrypted = aes_cbc_decrypt(key, iv, ct)
    >>> assert unpad(decrypted, 128) == pt
    """
    cipher = Cipher(algorithms.AES(key), mode=modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_pt = decryptor.update(ciphertext) + decryptor.finalize()
    return padded_pt


def XOR(array1: bytes, array2: bytes) -> bytes:
    """
    Performs the bitwise XOR operation on two given bytestrings.

    :param array1: The first operand.
    :param array2: The second operand.

    :returns: The bitwise XOR of ``array1`` and ``array2``.

    Example:

    >>> xor = XOR(bytes.fromhex('01ff'), bytes.fromhex('03fe'))
    >>> assert xor == bytes.fromhex('0201')
    """
    l = min(len(array1), len(array2))
    xored = bytes(a ^ b for (a, b) in zip(array1, array2))
    if len(array1) > l:
        xored += array1[l:]
    else:
        xored += array2[l:]
    return xored


def chacha20_encrypt(key: bytes, nonce: bytes, plaintext: bytes) -> bytes:
    """
    Use ChaCha20 to encrypt ``plaintext`` using ``key`` and ``nonce``.

    :param key: The bytes of the key (size 32 bytes)
    :param nonce: The bytes of the nonce (size 16 bytes)

    :returns: The bytes of the ciphertext.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(32)
    >>> nonce = secrets.token_bytes(16)
    >>> ciphertext = chacha20_encrypt(key=key, nonce=nonce, plaintext=b"message")
    """
    algorithm = algorithms.ChaCha20(key, nonce)
    encryptor = Cipher(algorithm, mode=None).encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def chacha20_decrypt(key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    """
    Use ChaCha20 to decrypt ``ciphertext`` using ``key`` and ``nonce``.

    :param key: The bytes of the key (size 32 bytes)
    :param nonce: The bytes of the nonce (size 16 bytes)

    :returns: The bytes of the plaintext.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(32)
    >>> nonce = secrets.token_bytes(16)
    >>> message = b"hello world"
    >>> ciphertext = chacha20_encrypt(key=key, nonce=nonce, plaintext=message)
    >>> assert message == chacha20_decrypt(key=key, nonce=nonce, ciphertext=ciphertext)
    """
    algorithm = algorithms.ChaCha20(key, nonce)
    decryptor = Cipher(algorithm, mode=None).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


# FIXME 2023: unify key, message vs key, plaintext in RSA
def aes_encrypt(key: bytes, message: bytes) -> bytes:
    """
    Use AES-CBC to encrypt ``message`` using ``key``.

    :param key: The bytes of the key (16, 24, 32 bytes in size).
    :param message: The message bytes to be encrypted.

    :returns: The bytes of the ciphertext.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(16)
    >>> ciphertext = aes_encrypt(key=key, message=b"my message")
    """
    padder = padding_symmetric.PKCS7(128).padder()
    padded_msg = padder.update(message) + padder.finalize()

    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(key=key), mode=modes.CBC(iv))
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded_msg) + encryptor.finalize()
    return iv + ciphertext


# FIXME argument is ciphertext, but the docs say message
def aes_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """
    Use AES-CBC to decrypt ``ciphertext`` using ``key``.


    :param key: The bytes of the key (16, 24, 32 bytes in size).
    :param message: The ciphertext bytes to be decrypted/

    :returns: The bytes of the plaintext.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(16)
    >>> message = b"hello world"
    >>> ciphertext = aes_encrypt(key=key, message=message)
    >>> assert message == aes_decrypt(key=key, ciphertext=ciphertext)
    """
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key=key), mode=modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding_symmetric.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext


def create_mac(key: bytes, data: bytes) -> bytes:
    """
    Calculate Message Authentication Code of ``data`` (using AES-CBC), i.e.
    encrypt ``data`` using ``key`` and AES-CBC with initialization vector
    equal to zero bytes.

    :param key: Is the AES symmetric key.
    :param data: Is the data that will be MAC'ed.

    :returns: 16 bytes long MAC value.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(32)
    >>> mac = create_mac(key=key, data=b"some data to MAC")
    """
    padder = padding_symmetric.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # the initialization vector is fixed to zero bytes
    iv = b"\x00" * 16
    cipher = Cipher(algorithms.AES(key=key), mode=modes.CBC(iv))

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # MAC is only the last block, i.e. 16 bytes
    mac = ciphertext[-16:]
    return mac


def verify_mac(key: bytes, data: bytes, mac: bytes) -> bool:
    """
    Verify that the MAC (using AES-CBC) of ``data`` matches ``mac``.

    :param key: Is the AES symmetric key.
    :param data: Is the data that will be MAC'ed.
    :param mac: Is the value against which we verify.

    :returns: ``True`` if the verification succeeds, ``False`` otherwise.

    Example:

    >>> import secrets
    >>> key = secrets.token_bytes(32)
    >>> data=b"some data to MAC"
    >>> mac = create_mac(key=key, data=data)
    >>> assert verify_mac(key=key, data=data, mac=mac)
    """
    return mac == create_mac(key=key, data=data)
