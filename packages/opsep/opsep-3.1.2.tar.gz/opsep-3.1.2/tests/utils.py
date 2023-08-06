import os
import requests

from pathlib import Path

from opsep import OPSEP_URL

# TODO: move test to own directory?
key_dir = Path(__file__).absolute().parent.parent

with open(os.path.join(key_dir, "insecureprivkey.pem"), "r") as f:
    PRIVKEY_STR = f.read()
with open(os.path.join(key_dir, "insecurepubkey.crt"), "r") as f:
    PUBKEY_STR = f.read()
