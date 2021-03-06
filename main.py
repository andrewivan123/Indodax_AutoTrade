# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests
import time
import hmac
import hashlib
import urllib


def get_ticker_last_price(name):
    """
    Parameters:
    -name: name of cryptocurrency in indodax. Example: btc, bnb,

    returns price of the specified cryptocurrency in idr
    """
    response_json = requests.get(f'https://indodax.com/api/ticker/{name}idr').json()
    if list(response_json.keys())[0] == 'error':
        raise NameError(f'{name} is not a valid ticker')
    else:
        return response_json['ticker']['last']


def get_wallet_balance_json(wait_time=5000):
    timestamp = int(time.time()*1000)
    payload = {'method': 'getInfo',
               'timestamp': timestamp,
               'recvWindow': timestamp+wait_time}
    message = bytes(urllib.parse.urlencode(payload),encoding='utf-8')
    #print(message)
    encrypted = hmac.new(key=b'3064d608c7df72f121f001c83b1da2835aeda4a5688a31fc198e80fcf01ba2d3270799e8bc8f8ec3',
                         msg=message, digestmod=hashlib.sha512).hexdigest()
    #print(encrypted)
    header = {'Key': 'LXREH1B7-CELQ9BDW-0QQWAKAD-2XXLFDUJ-NCAPAZLV', 'Sign': encrypted}
    response_json = requests.post('https://indodax.com/tapi', headers=header, data=payload)
    return response_json.json()['return']['balance']


def trade_ticker(type,name,wait_time=5000):
    """
    This function orders a buy or sell order of a particular cryptocurrency using the last price
    :param type: buy or sell
    :param name: name of cryptocurrency ticker in indodax
    :param wait_time: max wait time before timeout
    :return: status code of the trade order
    """
    timestamp = int(time.time() * 1000)
    if type == 'sell':
        payload = {'method': 'trade',
                   'timestamp': timestamp,
                   'recvWindow': timestamp + wait_time,
                   'pair': f'{name}_idr',
                   'type': 'sell',
                   'price': get_ticker_last_price(name),
                   'idr': '',
                   name: get_wallet_balance_json()[name]}
    message = bytes(urllib.parse.urlencode(payload), encoding='utf-8')
    # print(message)
    encrypted = hmac.new(key=b'3064d608c7df72f121f001c83b1da2835aeda4a5688a31fc198e80fcf01ba2d3270799e8bc8f8ec3',
                         msg=message, digestmod=hashlib.sha512).hexdigest()
    # print(encrypted)
    header = {'Key': 'LXREH1B7-CELQ9BDW-0QQWAKAD-2XXLFDUJ-NCAPAZLV', 'Sign': encrypted}
    response_json = requests.post('https://indodax.com/tapi', headers=header, data=payload)
    return response_json.status_code

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        time.sleep(1)
        last_price = int(get_ticker_last_price('matic'))
        print(last_price)
        if last_price < 2900:
            trade_ticker('sell','matic')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
