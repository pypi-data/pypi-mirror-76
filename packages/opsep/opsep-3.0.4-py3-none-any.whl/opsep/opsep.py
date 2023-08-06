import requests
import json

OPSEP_URL = "https://test.secondguard.com/"


class RateLimitError(Exception):
    pass


class BadRequestError(Exception):
    pass


def perform_asymmetric_decrypt_opsep(todecrypt_b64, opsep_url=OPSEP_URL):
    assert type(todecrypt_b64) is bytes, todecrypt_b64

    url = opsep_url + "api/v1/decrypt"
    payload = {
        "key_retrieval_ciphertext": todecrypt_b64.decode(),
    }

    # TODO: change protocol to not need this?
    headers = {"Content-Type": "application/json"}

    r = requests.post(url, json=payload, headers=headers)
    response = r.json()

    if r.status_code == 400:
        print(response)
        raise BadRequestError("Bad Request: %s" % response)

    if r.status_code == 429:
        print(response)
        raise RateLimitError("OpSep Rate Limit Exceeded: %s" % response)

    # Will throw an error if these fields don't exist
    return {
        "key_recovered": response["keyRecovered"],
        "request_sha256": response["requestSHA256"],
        "ratelimit_total": response["ratelimitTotal"],
        "ratelimit_remaining": response["ratelimitRemaining"],
        "ratelimit_resets_in": response["ratelimitResetsIn"],
    }


def fetch_pubkey(opsep_url=OPSEP_URL):
    return requests.get(url).json()['rsaPubKey']
