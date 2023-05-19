"""
The :py:mod:`asymmetric <pv080_crypto.asymmetric>` module defines the function for Asymmetric Cryptography or sometimes referred to as Public Key Cryptography. The functions :py:func:`publish_key <pv080_crypto.asymmetric.publish_key>` and :py:func:`fetch_key <pv080_crypto.asymmetric.fetch_key>` manage publishing and retrieving of the public key to the PV080 server. They allow you to share your public key and retrieve the keys of other students.

For asymmetric cryptography we are using the `Rivert-Shamir-Adleman <https://en.wikipedia.org/wiki/RSA_(cryptosystem)>`_ (RSA) cryptosystem. The functions for encryption and decryption are :py:func:`rsa_encrypt <pv080_crypto.asymmetric.rsa_encrypt>` and :py:func:`rsa_decrypt <pv080_crypto.asymmetric.rsa_decrypt>`.

The `asymmetric` nature of RSA allows for the definition of digital signatures as well, therefore we have the function :py:func:`create_signature <pv080_crypto.asymmetric.create_signature>` for creating the digital signature and :py:func:`verify_signature <pv080_crypto.asymmetric.verify_signature>` for verifying it.
"""
import hashlib
import requests

from binascii import hexlify, unhexlify
from typing import Optional

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import padding as padding_asymmetric
from cryptography.hazmat.primitives import hashes

from pv080_crypto.config import SERVER_KEY_PATH


def publish_key(uco: int, key: rsa.RSAPublicKey) -> str:
    """
    Publishes the ``key`` under the ``uco`` to https//pv080.fi.muni.cz/msg server,
    where it is readable by anyone on the internet.

    :param uco: Is the UČO of the owner of the key.
    :param key: Is the RSA public key of the owner.

    :returns: The status message of the result of this API call to the server.

    Example:

    >>> from cryptography.hazmat.primitives.asymmetric import rsa
    >>> private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    >>> public_key = private_key.public_key()
    >>> publish_key(uco=408788, key=public_key)
    'overwritten'
    """
    pem_key = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    resp = requests.post(
        SERVER_KEY_PATH,
        json={
            "uco": uco,
            "key": hexlify(pem_key).decode(),
        },
    )
    return resp.json()["status"]


def fetch_key(uco: int) -> Optional[rsa.RSAPublicKey]:
    """
    Fetches the public key associated with the ``uco`` from https://pv080.fi.muni.cz/msg.

    :param uco: Is the UČO of the party we want to communicate with.

    :returns: The ``rsa.RSAPublicKey`` corresponding to ``uco`` if found, otherwise ``None``.

    Example:

    >>> from cryptography.hazmat.primitives.asymmetric import rsa
    >>> private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    >>> public_key = private_key.public_key()
    >>> publish_key(uco=408788, key=public_key)
    'overwritten'
    >>> assert isinstance(fetch_key(uco=408788), rsa.RSAPublicKey)
    """
    resp = requests.get(
        SERVER_KEY_PATH,
        params={"uco": uco},
    )
    key: Optional[rsa.RSAPublicKey] = None
    data = resp.json()
    if "key" in data:
        key_bytes = bytes.fromhex(data["key"])
        serialized_key = serialization.load_pem_public_key(key_bytes)
        if isinstance(serialized_key, rsa.RSAPublicKey):
            key = serialized_key

    return key


# FIXME for 2023: return Optional[bytes] and return None on encryption failure?
def rsa_encrypt(key: rsa.RSAPublicKey, plaintext: bytes) -> bytes:
    """
    Uses RSA ``key`` to encrypt the ``plaintext``.

    :param key: Is the RSA public key to use for the encryption.
    :param plaintext: Is the plaintext bytes to be encrypted.

    :returns: The ciphertext bytes.

    Example:

    >>> from cryptography.hazmat.primitives.asymmetric import rsa
    >>> private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    >>> public_key = private_key.public_key()
    >>> ciphertext = rsa_encrypt(key=public_key, plaintext=b"hello world")
    """
    ciphertext = key.encrypt(
        plaintext,
        padding_asymmetric.OAEP(
            mgf=padding_asymmetric.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext


# FIXME for 2023: return Optional[bytes] and return None on decrypt failure?
def rsa_decrypt(key: rsa.RSAPrivateKey, ciphertext: bytes) -> bytes:
    """
    Use RSA public ``key`` to decrypt the ``ciphertext``.

    :param key: Is the RSA private key to use for the decryption.
    :param ciphertext: Is the ciphertext bytes to be decrypted.

    :returns: The plaintext bytes.

    Example:

    >>> from cryptography.hazmat.primitives.asymmetric import rsa
    >>> private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    >>> public_key = private_key.public_key()
    >>> ciphertext = rsa_encrypt(key=public_key, plaintext=b"hello world")
    >>> plaintext = rsa_decrypt(key=private_key, ciphertext=ciphertext)
    >>> assert b"hello world" == plaintext
    """
    plaintext = key.decrypt(
        ciphertext,
        padding_asymmetric.OAEP(
            mgf=padding_asymmetric.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return plaintext


def create_signature(private_key: rsa.RSAPrivateKey, data: bytes) -> bytes:
    """
    Use the RSA ``private_key`` to digitally sign the ``data``.

    :param private_key: Is an RSA private key.
    :param data: Is the data to be signed.

    :returns: The bytes of the signature.

    Example:

    >>> from cryptography.hazmat.primitives.asymmetric import rsa
    >>> private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    >>> public_key = private_key.public_key()
    >>> signature = create_signature(private_key=private_key, data=b"a contract contents")
    """
    prehashed_msg = hashlib.sha256(data).digest()
    signature = private_key.sign(
        prehashed_msg,
        padding_asymmetric.PSS(
            mgf=padding_asymmetric.MGF1(hashes.SHA256()),
            salt_length=padding_asymmetric.PSS.MAX_LENGTH,
        ),
        utils.Prehashed(hashes.SHA256()),
    )
    return signature


def verify_signature(
    public_key: rsa.RSAPublicKey, data: bytes, signature: bytes
) -> bool:
    """
    Verify that the ``signature`` of ``data`` was signed using the RSAPrivateKey
    corresponding to ``public_key``.

    :param public_key: Is the ``RSAPublicKey`` to be used for the verification.
    :param data: Is the data that were signed.
    :param signature: The bytes of the signature.

    :returns: ``True`` if the ``signature`` is a valid, ``False`` otherwise.

    Example:

    >>> from cryptography.hazmat.primitives.asymmetric import rsa
    >>> private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    >>> public_key = private_key.public_key()
    >>> data = b"the contract contents"
    >>> signature = create_signature(private_key=private_key, data=data)
    >>> assert verify_signature(public_key=public_key, data=data, signature=signature)
    """
    prehashed_msg = hashlib.sha256(data).digest()
    try:
        public_key.verify(
            signature,
            prehashed_msg,
            padding_asymmetric.PSS(
                mgf=padding_asymmetric.MGF1(hashes.SHA256()),
                salt_length=padding_asymmetric.PSS.MAX_LENGTH,
            ),
            utils.Prehashed(hashes.SHA256()),
        )
        return True
    except:
        return False
