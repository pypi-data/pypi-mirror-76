from base64 import b64decode
from datetime import datetime, timedelta
from hashlib import sha256
from os import urandom

from opsep import (
    opsep_hybrid_encrypt,
    opsep_hybrid_encrypt_with_auditlog,
    opsep_hybrid_decrypt,
    BadRequestError,
)

from tests.utils import PUBKEY_STR, _fetch_testing_pubkey


# TODO: add static decrypt test vectors

TESTING_RSA_PUBKEY = _fetch_testing_pubkey()


def _assert_valid_recovery_info(recovery_info_dict):
    # TODO: test actual rate limit behavior in recovery_info
    for k in ("ratelimit_total", "ratelimit_remaining", "ratelimit_resets_in"):
        assert type(recovery_info_dict[k]) is int, recovery_info_dict[k]

    # Confirm no other fields returned
    assert set(recovery_info_dict.keys()) == set(
        (
            "ratelimit_total",
            "ratelimit_remaining",
            "ratelimit_resets_in",
            "request_sha256",
        )
    )


def perform_opsep_hybrid_encryption_and_decryption_with_auditlog(
    secret, deprecate_at=None
):
    local_ciphertext, opsep_recovery_instructions, opsep_recovery_instructions_digest = opsep_hybrid_encrypt_with_auditlog(
        to_encrypt=secret,
        rsa_pubkey=TESTING_RSA_PUBKEY,
        deprecate_at=deprecate_at,
    )

    secret_recovered, recovery_info = opsep_hybrid_decrypt(
        local_ciphertext_to_decrypt=local_ciphertext,
        opsep_recovery_instructions=opsep_recovery_instructions,
    )

    assert secret == secret_recovered
    assert (
        opsep_recovery_instructions_digest == recovery_info["request_sha256"]
    )
    _assert_valid_recovery_info(recovery_info)


def perform_opsep_hybrid_encryption_and_decryption(secret, deprecate_at=None):
    local_ciphertext, opsep_recovery_instructions = opsep_hybrid_encrypt(
        to_encrypt=secret,
        rsa_pubkey=TESTING_RSA_PUBKEY,
        deprecate_at=deprecate_at,
    )

    secret_recovered, recovery_info = opsep_hybrid_decrypt(
        local_ciphertext_to_decrypt=local_ciphertext,
        opsep_recovery_instructions=opsep_recovery_instructions,
    )

    assert secret == secret_recovered
    # sha256(opsep_recovery_instructions) matches returned:
    assert (
        sha256(b64decode(opsep_recovery_instructions)).hexdigest()
        == recovery_info["request_sha256"]
    )
    _assert_valid_recovery_info(recovery_info)


def test_opsep_hybrid_encryption_and_decryption():
    secret = urandom(1000)
    future_expiry = datetime.now() + timedelta(days=100)
    past_expiry = datetime.now() - timedelta(days=100)

    for deprecate_at in (None, future_expiry):
        perform_opsep_hybrid_encryption_and_decryption(
            secret=secret, deprecate_at=deprecate_at
        )
        perform_opsep_hybrid_encryption_and_decryption_with_auditlog(
            secret=secret, deprecate_at=deprecate_at
        )

    # Confirm that an expired key throws an error:
    try:
        perform_opsep_hybrid_encryption_and_decryption(
            secret=secret, deprecate_at=past_expiry
        )
        assert False
    except BadRequestError:
        assert True

    try:
        perform_opsep_hybrid_encryption_and_decryption_with_auditlog(
            secret=secret, deprecate_at=past_expiry
        )
        assert False
    except BadRequestError:
        assert True
