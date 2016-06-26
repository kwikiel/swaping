import hmac
import time
import urllib
import hashlib
import requests

import config


class BitapiException(Exception):
    pass


class Yolo():

    def __init__(self, key=config.key, secret=config.secret):
        self.key = key
        self.secret = secret

    def bitapi(self, method, **params):
        """Main method for bitmarket API"""
        endpoint = "https://www.bitmarket.pl/api2/"
        times = int(time.time())
        params.update({
            "method": method,
            "tonce": times,
            "currency": "BTC"
            })

        post = urllib.urlencode(params)
        sign = hmac.HMAC(
            str(self.secret), post, digestmod=hashlib.sha512).hexdigest()
        headers = {"API-Key": str(self.key), "API-Hash": sign}
        raw = requests.post(endpoint, data=post, headers=headers)

        if 'error' in raw.json():
            raise BitapiException(raw.json())
        return raw.json()

    def get_cutoff(self):
        """Returns max profit for swaps """
        raw = requests.get("http://bitmarket.pl/json/swapBTC/swap.json")
        return raw.json()["cutoff"]

    def cancel_all(self):
        """Powerful: cancels all open swaps """
        swap_list = self.bitapi("swapList")["data"]

        for swap in swap_list:
            self.bitapi("swapClose", id=swap["id"])

    def make_best(self):
        # Uses magic contant, remove later.
        rclear = '%.4f' % float(self.get_cutoff()*0.95)
        if self.get_balance()<0.01:
            print "Nothing to do here. No money"
        else:
            print 'RATE: %s' % rclear
            return self.bitapi(
               'swapOpen',
               amount=float(self.get_balance()),
               rate=rclear)

    def swap_list(self):
        """Listing all open offers with nice interface"""
        swap_list_data = self.bitapi("swapList")["data"]
        return swap_list_data

    def get_info(self):
        return self.bitapi('info')

    def get_balance(self):
        return self.bitapi('info')['data']['balances']['available']['BTC']
