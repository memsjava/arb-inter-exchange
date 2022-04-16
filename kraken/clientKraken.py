import requests
import json


def getOrderbook(pair):
    resp = requests.get('https://api.kraken.com/0/public/Depth?pair='+pair)
    resp = resp.json()
    if pair == 'XRPUSD':
        pair = 'XXRPZUSD'
    resp = resp['result'][pair]

    return resp
