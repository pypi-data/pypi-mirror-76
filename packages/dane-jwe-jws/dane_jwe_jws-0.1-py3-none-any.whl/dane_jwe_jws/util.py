"""General-purpose utilities."""
import binascii

from dane_discovery.dane import DANE
from jwcrypto import jwk


class Util:
    """General-purpose utilities."""

    @classmethod
    def build_dns_uri(cls, device_id):
        """Return a DNS URI for the device identity."""
        kid = "dns://{}?type=TLSA".format(device_id)
        return kid

    @classmethod
    def get_name_from_dns_uri(cls, dns_uri):
        """Return the DNS name from dns_uri.

        Support hostname extraction from input format consistent with relative
        and authoritative records as defined in
        https://tools.ietf.org/html/rfc4501.

        Args:
            dns_uri (str): DNS URI.

        Return:
            str: DNS name.

        Raise:
            ValueError: If format is wrong, raise an error.
        """
        preamble = "dns:"
        ending = "?type=TLSA"
        if not dns_uri.startswith(preamble):
            raise ValueError("Bad format. See RFC 4501.")
        if not dns_uri.endswith(ending):
            raise ValueError("Bad format. See RFC 4501.")
        reduced = dns_uri.replace(preamble, "").replace(ending, "")
        hostname = reduced.split("/")[-1]
        return hostname

    @classmethod
    def get_pubkey_from_dns(cls, dns_name):
        """Return JWK from DNS record.

        Args:
            dns_name (str): DNS name for locating TLSArr.

        Return:
            JWK: Javascript Web Key containing public
                key retrieved from DNS.

        """
        tlsa = DANE.get_first_leaf_certificate(dns_name)
        der = binascii.unhexlify(tlsa["certificate_association"])
        cert_pem = DANE.der_to_pem(der)
        pubkey = jwk.JWK()
        pubkey.import_from_pem(cert_pem)
        return pubkey
