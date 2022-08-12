"""
    This library is still in the process of being created. It is not recommended to use it yet in development.

Author: Josué Carballo Baños
License: GNU GPL from the Free Software Foundation v3 and later.
"""

import base64
from io import BytesIO
import requests
import qrcode
import json

from requests import Timeout


class enzona_api():
    token = None
    consumer_key = None
    consumer_secret = None

    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token = self.get_token()

    def get_token(self):
        """
        :return: Returns an API access token It depends on the input of the public and private keys.
        """
        bs4 = self.get_base64(self.consumer_key + ":" + self.consumer_secret)
        data = {
            "grant_type": "client_credentials",
            'scope': 'enzona_business_payment'
        }
        headers = {
            "Authorization": "Basic " + bs4.split("'")[1]
        }
        response = requests.post("https://api.enzona.net/token", data=data,
                                 headers=headers)
        try:
            if response.status_code != 200:
                return response.reason
            else:
                json_response = response.json()
                self.token = json_response["access_token"]
                return json_response['access_token']

        except ConnectionError as error:
            return {'success': False, 'error': 'Network Error',
                    'error_detail': error}
        except Timeout as error:
            return {'success': False, 'error': 'Network Conection Timeout',
                    'error_detail': error}

    @staticmethod
    def get_base64(text):
        return str(base64.b64encode(bytes(text, "utf-8"))).__str__()
