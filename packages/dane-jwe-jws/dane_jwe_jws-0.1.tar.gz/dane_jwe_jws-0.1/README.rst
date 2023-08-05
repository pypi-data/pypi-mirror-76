============
dane_jwe_jws
============

A library for using JWE and JWS with DANE for identity-secured messaging.


This library enables the easy generation of signed and encrypted messages,
using TLSA records in DNS for public key discovery. This library places the
DNS URI in the ``x5u`` protected header field. The receiving party uses this
field for discovering the public key which is used for verifying message
payload.

.. image:: https://readthedocs.org/projects/dane-jwe-jws/badge/?version=latest
    :target: https://dane-jwe-jws.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


.. image:: https://api.codeclimate.com/v1/badges/8a46b39865a6f88dc31c/maintainability
   :target: https://codeclimate.com/github/ValiMail/dane_jwe_jws/maintainability
   :alt: Maintainability


.. image:: https://api.codeclimate.com/v1/badges/8a46b39865a6f88dc31c/test_coverage
   :target: https://codeclimate.com/github/ValiMail/dane_jwe_jws/test_coverage
   :alt: Test Coverage


Quick Start
===========

Installation
------------

``pip install dane-jwe-jws``


Encrypt a message using a DANE-represented identity
---------------------------------------------------

.. code-block:: python

    from dane_jwe_jws.encryption import Encryption
    test_message = "hello world!!"
    identity_name = "dns.name.where.cert.lives.in.a.tlsa.record"
    encrypted = Encryption.encrypt(test_message, identity_name)
    print(encrypted)


`More examples <https://dane-jwe-jws.readthedocs.io/en/latest/getting_started.html>`_
