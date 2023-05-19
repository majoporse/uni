import pathlib

from typing import List, Optional, Union, Tuple

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes


def store_private_key(
    private_key: rsa.RSAPrivateKey,
    filename: str = "private_key.pem",
    overwrite: bool = False,
) -> bool:
    """
    Stores an RSA private key in a given file.

    :param rsa.RSAPublicKey private_key: RSA key to store.
    :param str filename: Filename to store the key into.
    :param bool overwrite: Flag to determine whether we want to overwrite an existing file.

    :returns: True if the `private_key` is written into `filename`, False otherwise.
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    if not pathlib.Path(filename).exists() or overwrite:
        with open(filename, "wb") as handle:
            handle.write(pem)
        return True

    return False


def load_private_key(
    filename: str = "private_key.pem",
) -> rsa.RSAPrivateKey:
    """
    Loads a private key from a given file.

    :param str filename: Filename to look for the key in.
    :returns: The private key itself.
    """
    filepath = pathlib.Path(filename)
    with open(filepath, "rb") as key_file:
        pem_data = key_file.read()

    private_key = serialization.load_pem_private_key(
        pem_data,
        password=None,
    )
    return private_key


def store_cert(
    cert: x509.Certificate,
    filename: str,
    overwrite: bool = False,
) -> bool:
    """
    Stores an x509 certificate in a given file.

    :param X509.Certificate cert: Certificate to store.
    :param str filename: Filename to store the certificate into.
    :param bool overwrite: Flag to determine whether we want to overwrite an existing file.

    :returns: True if the `cert` is written into `filename`, False otherwise.
    """
    if not pathlib.Path(filename).exists() or overwrite:
        with open(filename, "wb") as handle:
            handle.write(cert.public_bytes(serialization.Encoding.PEM))
        return True

    return False


def load_cert(filename: str) -> x509.Certificate:
    """
    Loads a certificate from a given file.

    :param str filename: Filename to look for the certificate in.

    :returns: The certificate itself.
    """
    filepath = pathlib.Path(filename)
    with open(filepath, "rb") as cert_file:
        pem_data = cert_file.read()

    cert = x509.load_pem_x509_certificate(pem_data)
    return cert


def extract_names(cert: x509.Certificate) -> Tuple[Optional[int], Optional[str]]:
    """
    Extracts UČO and xlogin from a certificate.

    :param X509.Certificate cert: The certificate to extract names from.

    :returns Tuple[Optional[int], Optional[str]]: A tuple of UČO and xlogin, if present in the certificate.
    """
    common_names = [
        name.value for name in cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
    ]
    uco: Optional[int] = None
    # guess and hope
    for name in common_names:
        try:
            uco = int(name)
            break
        except:
            pass

    xlogin: Optional[str] = None
    for name in common_names:
        if name.strip().startswith("x"):
            xlogin = name
            break

    return uco, xlogin


def create_csr(
    key: rsa.RSAPrivateKey, xlogin: str, uco: int
) -> x509.CertificateSigningRequest:
    """
    Creates a Certificate Signing Request with given names.

    param rsa.RSAPrivateKey key: The key to sign the CSR with. The corresponding public key is the certified one.
    param str xlogin: xlogin to insert as a name into the request.
    param int uco: UČO to insert as a name into the request.
    return x509.CertificateSigningRequest: The CSR itself.
    """
    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(
            x509.Name(
                [
                    # Provide various details about who we are.
                    x509.NameAttribute(NameOID.COUNTRY_NAME, "CZ"),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "South Moravia"),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, "Brno"),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "PV080"),
                    x509.NameAttribute(NameOID.COMMON_NAME, str(uco)),
                    x509.NameAttribute(NameOID.COMMON_NAME, xlogin),
                ]
            )
        )
        .sign(key, hashes.SHA256())
    )

    return csr
