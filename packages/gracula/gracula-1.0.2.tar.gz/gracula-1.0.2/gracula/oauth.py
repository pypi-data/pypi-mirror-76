import time
import random
import hashlib
import urllib.request
from urllib.parse import urlencode, quote
import base64
import hmac
import json


class TwitterOAuth:
    oauth_signature_method = 'HMAC-SHA1'
    oauth_version = '1.0'
    oauth_params = None

    def __init__(self, consumer_key: str, consumer_secret: str, access_token: str, access_secret_key: str):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret_key = access_secret_key

    def set_oauth_params(self):
        self.oauth_params = {
            "oauth_token": self.access_token,
            "oauth_consumer_key": self.consumer_key,
            "oauth_signature_method": self.oauth_signature_method,
            "oauth_timestamp": self.oauth_timestamp,
            "oauth_nonce": self.oauth_nonce,
            "oauth_version": self.oauth_version
        }

    def response(self, url, method, params):
        self.set_oauth_params()

        header = self.request_header(method=method, url=url, params=params)
        request = urllib.request.Request(url=url + '?' + urlencode(params), headers=header, method=method)

        with urllib.request.urlopen(request) as response:
            return json.load(response)

    @property
    def oauth_timestamp(self):
        return str(int(time.time()))

    @property
    def oauth_nonce(self):
        return str(random.getrandbits(64))

    @staticmethod
    def join_params_equal_format(join_str: str, params: dict) -> str:
        return join_str.join('{0}={1}'.format(quote(key, ''), quote(params[key], '~')) for key in sorted(params))

    def oauth_signature(self, method: str, url: str, params: dict):
        oauth_params = self.oauth_params
        oauth_params.update(params)
        signature = self.join_params_equal_format('&', oauth_params)

        return base64.b64encode(
            hmac.new(
                bytes('{0}&{1}'.format(self.consumer_secret, self.access_secret_key), 'UTF-8'),
                bytes('{0}&{1}&{2}'.format(method.upper(), quote(url, ''), quote(signature, '')), 'UTF-8'),
                hashlib.sha1).digest()
        )

    def request_header(self, method: str, url: str, params: dict) -> dict:
        oauth_params = self.oauth_params
        oauth_signature = self.oauth_signature(method=method, url=url, params=params)
        oauth_params.update({'oauth_signature': oauth_signature})
        header = self.join_params_equal_format(',', oauth_params)
        return {"Authorization": 'OAuth {0}'.format(header)}
