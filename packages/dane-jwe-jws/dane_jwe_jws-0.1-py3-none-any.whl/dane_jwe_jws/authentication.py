"""Authentication-related functionality."""
import json

from jwcrypto import jwk, jws

from .util import Util


class Authentication:
    """This class wraps functions for message authentication."""

    @classmethod
    def sign(cls, message, private_key, dane_id, header_field="x5u"):
        """Return a signed JWS message.

        Args:
            message (str): Message to be encapsulated and signed.
            private_key (str): Path to private key in PEM format.
            dane_id (str): DANE identity where the signature verification
                public key can be located.
            header_field (str): Name of the header field used for storing
                DANE URI. Defaults to ``x5u``.

        Return:
            (str): Signed and serialized JWS.

        """
        with open(private_key, "rb") as priv_key_file:
            privkey_pem = priv_key_file.read()
        privkey_jwk = jwk.JWK()
        privkey_jwk.import_from_pem(privkey_pem)
        dns_uri = Util.build_dns_uri(dane_id)
        protected = {"alg": "RS256", header_field: dns_uri}
        jwstoken = jws.JWS(message.encode('utf-8'))
        jwstoken.add_signature(privkey_jwk, None, protected)
        signed = jwstoken.serialize()
        return signed

    @classmethod
    def verify(cls, message, header_field="x5u"):
        """Return original message if signature checks out, or raise and error.

        Args:
            message (str): Serialized JWS message.
            header_field (str): Header field where DANE URI can be found.
                Defaults to ``x5u``.

        Return:
            str: Payload extracted from signed message.

        Raise:
            jwcrypto.jws.InvalidJWSSignature if signature fails

        """
        jwstoken = jws.JWS()
        jwstoken.deserialize(message)
        print("JWS header: {}".format(json.dumps(jwstoken.jose_header)))
        dns_uri = jwstoken.jose_header[header_field]
        key = Util.get_pubkey_from_dns(dns_uri)
        jwstoken.verify(key)
        payload = jwstoken.payload
        return payload
