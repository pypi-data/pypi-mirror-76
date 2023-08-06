# OpSep Python Client Library

In order to use this client library, you will need to be running an [OpSep Server](https://github.com/opsep/opsep-server) to protect your RSA private key.

For simplicty, we'll use an OpSep server hosted by SecondGuard at https://test.secondguard.com/, along with its corresponding RSA public key.
Note that this is **not** suitable for production data, the RSA private key has been published!

## Quickstart

Install from [PyPI](https://pypi.org/project/opsep/):
```bash
$ pip3 install --upgrade opsep
```

Encrypt using the testing API token and testing RSA pubkey (no account needed):
```python
from opsep import opsep_hybrid_encrypt, opsep_hybrid_decrypt

# Testing RSA PubKey and OpSep API Server URL (normally saved in your app's config)
RSA_PUBKEY = '-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA7q4R3soRD2CrjL13OK6Y\nSBG8wpjP5sbfkL0QhpJMH87grlR2SS3CUnbYCOONzQiJ3OuKAViy/lMw1KsmG9Nn\nhAot2acg1iNyZRY33LR2jwmfFF+2iRp0itPQeOHY6GS8m3WLCMtC/kWUq0Bl5g1P\nYa9JXwSkTTRJunNH0TPk8uqwFeVhpT336M1H6ed105L8a8W3mpSwlwePron7pLf7\nwD32m9RT0nNdnHBDQCsUKS/Gdp+saLYWTgj0rpnQCe8f1p3g36Gm0gTzr3X0Adow\n8gIPfxO4HU/0cdL+Pw4mpcsWJ4531taRLLGb+a2la2zAUteYcS+8d4Nb8Omkbz39\nPylvKP6R1kHElqlF3BnwUp0AdcAvOLdeX8kYUlbKE8xwjHm/KwwleKlcAZDam7hC\nRw72JUQiod0E7My+SiZ3Ij5zKnxZXmAF5BX8T+YSqSzR4Qdp2QU9L9GgAZo/HPBN\nwME9v8usjEzrEItSSg3Nn10+J+ygsCqjrCT8CnSvD8wEyDSdO/Jly9DnWJ6B2HJE\nOc4wxWGFTCE0wiQOwC3IPNxFhuWun6/4tsEQcDs5XHaBXIHry5WCiVkjwa2pc95x\niXcfoQWr1A/jLe/MrZyN4yrgDK9mmQxxNzVfLj8S9NPjJMv+K7BKvtOmvoqsf13K\n6hYJGkAdR0d99DNFlllRm7cCAwEAAQ==\n-----END PUBLIC KEY-----\n'
OPSEP_URL = 'https://test.secondguard.com/'

your_secret = b"attack at dawn!"

# Encrypt locally (symmetrically and asymmetrically) and save the results to your DB:
local_ciphertext, opsep_recovery_instructions = opsep_hybrid_encrypt(
    to_encrypt=your_secret,
    rsa_pubkey=RSA_PUBKEY, 
)

# Asymmetrically decrypt opsep_recovery_instructions (via OpSep's rate-limited API) and use it to symmetrically decrypt local_ciphertext: 
secret_recovered, rate_limit_info = opsep_hybrid_decrypt( 
    local_ciphertext_to_decrypt=local_ciphertext, 
    opsep_recovery_instructions=opsep_recovery_instructions,
    opsep_url=OPSEP_URL,
)

if your_secret == secret_recovered:
    print("Your secret was recovered: %s" % secret_recovered)
```

See [test_client.py](https://github.com/opsep/opsep-python/blob/master/tests/test_client.py) to see how the protocol works.

### Audit Log
For audit logging of decryption requests, we recommend storing the sha256 hash digest of the `opsep_recovery_instructions` (base64 decoded) in an indexed column of your database. This makes it easy to see which records have been decrypted if your servers are breached. See the `opsep_hybrid_encrypt_with_auditlog()` method with test coverage in [test_client.py](https://github.com/opsep/opsep-python/blob/master/tests/test_client.py).


---

## Under the Hood

Pull requests with test coverage are welcome!

Check out the code:
```bash
$ git checkout git@github.com:opsep/opsep-python.git && cd opsep-python.git
```

Create & activate a virtual environment, install dependencies & this library
```bash
$ python3 -m virtualenv .venv3 && source .venv3/bin/activate && pip3 install -r requirements.txt && pip3 install --editable .
```

Run tests (requires having previously intalled an `--editable` local version of this repo):
```
$ pytest -v
====================================== test session starts ======================================
platform darwin -- Python 3.7.8, pytest-5.4.3, py-1.9.0, pluggy-0.13.1 -- /Users/mflaxman/workspace/secondguard-python/.venv3/bin/python
cachedir: .pytest_cache
rootdir: /Users/mflaxman/workspace/opsep-python
collected 3 items                                                                               

tests/test_client.py::test_opsep_hybrid_encryption_and_decryption PASSED                  [ 33%]
tests/test_pyca.py::test_symmetric PASSED                                                 [ 66%]
tests/test_pyca.py::test_asymmetric PASSED                                                [100%]
```

To update `requirements.txt` change `requirements.in` and then run (requires [pip-tools](https://github.com/jazzband/pip-tools)):
```bash
$ pip-compile requirements.in
```

How these **insecure** testing RSA keys were created:
```bash
$ openssl genrsa -out insecureprivkey.pem 4096 && openssl rsa -in insecureprivkey.pem -pubout -out insecurepubkey.crt
```
