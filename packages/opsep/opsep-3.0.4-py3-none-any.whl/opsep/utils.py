import requests
from hashlib import sha256

HEX_CHARS = set("0123456789abcdef")



def _assert_valid_pubkey(pubkey_str):
    assert type(pubkey_str) is str, pubkey_str
    assert pubkey_str.strip().startswith("-----BEGIN PUBLIC KEY-----"), pubkey_str
    assert pubkey_str.strip().endswith("-----END PUBLIC KEY-----"), pubkey_str


def _assert_valid_privkey(privkey_str):
    assert type(privkey_str) is str, privkey_str
    assert privkey_str.strip().startswith(
        "-----BEGIN RSA PRIVATE KEY-----"
    ), privkey_str
    assert privkey_str.strip().endswith("-----END RSA PRIVATE KEY-----"), privkey_str


def _assert_same(input1, input2):
    if input1 != input2:
        raise Exception("Have: %s\nWant: %s" % (input1, input2))
