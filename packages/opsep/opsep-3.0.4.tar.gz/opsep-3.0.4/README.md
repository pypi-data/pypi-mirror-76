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

your_secret = b"attack at dawn!"

# Testing RSA PubKey and OpSep API Server URL (normally saved in your app's config)
RSA_PUBKEY = '''-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxY9sgHqrHRkfppnOJACr\nhwYxHP4d/OUUzbTiNFfcFoCyCUCL6dnLql1WPfaUyYWeLEQ4NTFI9Nfdy9tka6ZO\n75V3LCW5l2TMkbb0BvWnAcIK3lMY19kfFyImAoLvcZcAevi0ogkOn20zDrxVhlpv\nQAu3OMCQmc1aMgv6pp1FO4v3OjiXNp1AQQw8CIHnQzlLmGSMeUK1hdCcSGXq5qLA\nXrKwdkA8K6gDi67A43ZcWzew1KF8OwtA2WyLRfbzGaXqqq2pLNcrt90v64azkk+Q\nn8JTJym7k30Jv7zbhsGR08dvk6zn7TrNMn1TsIwflDFGSpzSCAQcz1gR+0GiwGvk\nqQkKeNhTAUHOdf7IONEpmZ+46O4uUmtAXu5lI0D5dPtl2M5ZtAjxRMvXX65QeNd7\nMwcoXy5LaUMnDVl8Sq8OL8dj8PMKiqO7m/yMuMfXgEd9EcdzFt80rRUCH3/H3+MT\nQMZdlbNASA5d//MOxERsb1ildEyfTQpSWvyeGIpCCtPmq3yJbKat95RTUX4uJPLi\nKFCifkVhirl+XxdDK6L0gly0kZEW41qyKZL+++5M6NalsBsMr5AFAUF0Ws4E+aWf\n6Zm8FDi6G4ZpAmVpP6bmqY+GoTFBQKXezICAwsJ6Dhy8UUHxDRQIiNTSLVnO5wgR\ncRfaU/jG6gorIFQvw8mw2hcCAwEAAQ==\n-----END PUBLIC KEY-----\n'''
OPSEP_URL = 'https://test.secondguard.com/'

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
