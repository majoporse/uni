from typing import Optional, Tuple

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa


def verify_cert_signature(
    ca_public_key: rsa.RSAPublicKey,
    cert: x509.Certificate,
) -> bool:
    """
    Verifies whether the certificate was signed by the Certificate Authority whose public key is provided.

    :param ca_public_key: is the public key of the Certificate Authority, used to verify the signature.
    :param cert: is the subject of the verification, the certificate to be checked.
    :returns: ``True`` if ``cert`` was signed with private key corresponding to ``ca_public_key``, ``False`` otherwise.

    Example:

    >>> # doctest: +SKIP
    >>> from pv080_crypto import verify_cert_signature, fetch_cert
    >>> from pv080_crypto.utils import load_cert
    >>> ca_cert = load_cert("pv080-root.pem")
    >>> ca_public_key = ca_cert.public_key()
    >>> cert = fetch_cert(410390)
    >>> print(verify_cert_signature(ca_public_key, cert))
    """
    try:
        ca_public_key.verify(
            cert.signature,
            cert.tbs_certificate_bytes,
            padding_asymmetric.PKCS1v15(),
            cert.signature_hash_algorithm,
        )
        return True
    except:
        return False


# FIXME: creating the file name is enough for our purposes, no need
#        to bother with the content as well?
# FIXME improve the verification
# FIXME: missing example
def request_cert(
    csr: x509.CertificateSigningRequest,
) -> Optional[Tuple[str, str, bytes]]:
    """
    Request a certificate from CA using provided certificate signing request.

    :param csr: is the Certificate Signing Request (created with the ``create_csr`` method).

    :returns: ``None`` if unsuccessful, challenge otherwise.
    The challenge is a tuple with three elements:

    - ``path`` is a string containing a random path to a file. \
        to prove that you are, indeed, the person with xlogin,\
        you must create this file on your aisa web server.

    - ``content`` is a string that must be saved as a content of the file\
        sitting on ``path``. (Since only you have the access to your `Aisa <https://www.fi.muni.cz/tech/unix/aisa.html.en>`_ web server,\
        this counts as a proof of your identity.)

    - ``nonce`` are random bytes. By signing this nonce, you prove that you\
        hold the corresponding private key.
    """
    data = {"csr": csr.public_bytes(serialization.Encoding.PEM).hex()}
    response = requests.post(SERVER_CERT_REQUEST_CHALLENGE, json=data)

    if response.json()["status"] != "OK":
        print(response.json()["status"])
        return None

    path = response.json()["path"]
    content = response.json()["content"]
    nonce = bytes.fromhex(response.json()["nonce"])
    return path, content, nonce


# FIXME: missing example
def verify_challenge(nonce: bytes, signed_nonce: bytes) -> bool:
    """
    Verifies that given nonce was issued as a challenge and checks that it was signed by the private key of the
    challenged entity.

    :param nonce: nonce to be signed with the private key of the challenged entity.
    :param signed_nonce: Signature of the nonce.

    :returns: ``True`` if verified successfully, ``False`` otherwise.
    """
    response = requests.post(
        SERVER_CERT_VERIFY_CHALLENGE,
        json={"nonce": nonce.hex(), "signed_nonce": signed_nonce.hex()},
    )
    print(response.json()["status"])
    return response.json()["status"] == "OK"


# FIXME: missing example
def fetch_cert(uco: int) -> Optional[x509.Certificate]:
    """
    Fetches a certificate for given UCO from PV080 server.

    :param uco: is the identifier of the person whose certificate is going to be fetched.

    :returns: the certificate from the PV080 corresponding to the ``uco``, ``None`` if no such certifiate is found.
    """
    response = requests.get(SERVER_CERTIFICATES, params={"uco": uco})

    if response.json()["status"] != "OK":
        print(response.json()["status"])
        return None

    cert_pem = response.json()["certificate"]
    cert = x509.load_pem_x509_certificate(cert_pem.encode())
    return cert
