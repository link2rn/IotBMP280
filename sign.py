from base64 import b64encode, b64decode
from hashlib import sha256
from urllib import quote_plus, urlencode
from hmac import HMAC
import requests
import json
import os
import time

def generate_sas_token():
    URI="sochwarestation.azure-devices.net"
    KEY="2kT5rApjq3c7LQr/Tq35Of29gtp7/ddpIlgYfvkErEs="
    POLICY = 'iothubowner'
    expiry=3600
    ttl = time.time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(URI)), int(ttl))
    signature = b64encode(HMAC(b64decode(KEY), sign_key, sha256).digest())

    rawtoken = {
        'sr' :  URI,
        'sig': signature,
        'se' : str(int(ttl))
    }

    rawtoken['skn'] = POLICY

    return 'SharedAccessSignature ' + urlencode(rawtoken)
print(generate_sas_token())
