"""Encryption-related functionality."""
from jwcrypto import jwk, jwe

from .util import Util


class Encryption:
    """This class wraps functions for message encryption."""

    @classmethod
    def decrypt(cls, message, private_key):
        """Return a decrypted message.

        Args:
            message (str): JWE to be decrypted.
            private_key (str): Path to private key.

        Return:
            str: Decrypted contents of JWE.

        """
        with open(private_key, "rb") as priv_key_file:
            privkey_pem = priv_key_file.read()
        token = jwe.JWE()
        privkey_jwk = jwk.JWK()
        privkey_jwk.import_from_pem(privkey_pem)
        token.deserialize(message, key=privkey_jwk)
        payload = token.payload
        return payload.decode()

    @classmethod
    def encrypt(cls, message, dane_id, header_field="x5u"):
        """Return True if the message signature is valid, otherwise False.

        Args:
            message (str): Message to be encrypted.
            dane_id (str): DANE identity for locating encryption key.
            header_field (str): Header field where DANE URI can be found.
                Defaults to ``x5u``.

        Return:
            str: Encrypted and serialized JWE.

        """
        pubkey = Util.get_pubkey_from_dns(dane_id)
        protected_header = {"alg": "RSA-OAEP-256",
                            "enc": "A256CBC-HS512",
                            "typ": "JWE",
                            "x5u": Util.build_dns_uri(dane_id)}
        jwetoken = jwe.JWE(message.encode("utf-8"),
                           recipient=pubkey,
                           protected=protected_header)
        return jwetoken.serialize()
