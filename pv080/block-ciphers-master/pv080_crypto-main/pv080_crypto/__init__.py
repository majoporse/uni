"""
The ``pv080_crypto`` package contains the modules and functions that will be
used during the cryptography-related seminars in the course PV080 Information
Security and Cryptography.


The :py:mod:`messaging <pv080_crypto.messaging>` module contains the functions
for communicating with the https://pv080.fi.muni.cz server. The functions
concerned with symmetric encryption/decryption (mostly AES) and MACs are in
:py:mod:`symmetric <pv080_crypto.symmetric>`.

The ``pv080_crypto`` is built on top of the Python `cryptography
<https://cryptography.io/en/latest/>`_ module.
"""

# TODO: Add the following docs once they are needed.
asymmetric_and_certs_docs = """and the asymmetric ones (for RSA) are in
:py:mod:`asymmetric <pv080_crypto.asymmetric>`. The handling of certificates is in
:py:mod:`certificates <pv080_crypto.certificates>`.
"""

utilities_docs = """
Some utility functions can be found in :py:mod:`utils <pv080_crypto.utils>`.

"""

# FIXME Format the link to Pyca cryptography nicer.

from pv080_crypto.messaging import send_message, recv_message
from pv080_crypto.symmetric import (
    pad,
    unpad,
    aes_ecb_encrypt,
    aes_ecb_decrypt,
    aes_cbc_encrypt,
    aes_cbc_decrypt,
    XOR,
    chacha20_encrypt,
    chacha20_decrypt,
    aes_encrypt,
    aes_decrypt,
    create_mac,
    verify_mac,
)
from pv080_crypto.asymmetric import (
    publish_key,
    fetch_key,
    rsa_encrypt,
    rsa_decrypt,
    create_signature,
    verify_signature,
)
from pv080_crypto.utils import (
    store_private_key,
    load_private_key,
    store_cert,
    load_cert,
    extract_names,
    create_csr,
)
from pv080_crypto.certificates import (
    verify_cert_signature,
    request_cert,
    verify_challenge,
    fetch_cert,
)

__all__ = [
    # messaging
    "send_message",
    "recv_message",
    # symmetric
    "pad",
    "unpad",
    "aes_ecb_encrypt",
    "aes_ecb_decrypt",
    "aes_cbc_encrypt",
    "aes_cbc_decrypt",
    "XOR",
    "chacha20_encrypt",
    "chacha20_decrypt",
    "aes_encrypt",
    "aes_decrypt",
    "create_mac",
    "verify_mac",
    # asymmetric
    "publish_key",
    "fetch_key",
    "rsa_encrypt",
    "rsa_decrypt",
    "create_signature",
    "verify_signature",
    # certificates
    "verify_cert_signature",
    "request_cert",
    "verify_challenge",
    "fetch_cert",
    # utils
    "store_private_key",
    "load_private_key",
    "store_cert",
    "load_cert",
    "extract_names",
    "create_csr",
]
