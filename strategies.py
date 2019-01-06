import json
import re
import hashlib
from abc import ABC, abstractmethod

import requests
from flask import render_template, flash, redirect, url_for

from config import DevelopmentConfig as Config


class AbstractStrategy(ABC):
    def __init__(self):
        self._required_fields = tuple()

    @abstractmethod
    def execute(self, params=None):
        pass

    def create_sign_key(self, params):
        print("Error field not in:  ", set(self._required_fields) - set(params.keys()))
        assert params.keys() >= set(self._required_fields)
        s = ':'.join(str(params.get(k, '')) for k in self._required_fields) + Config.SECRET
        m = hashlib.sha256()
        m.update(s.encode())
        return m.hexdigest()


class EuroStrate(AbstractStrategy):
    def __init__(self):
        self._required_fields = sorted({'amount', 'currency', 'shop_id', 'shop_order_id'})

    def execute(self, params=None):
        # create html form
        params.update({'currency': 978})
        print(f"Params: {params}")
        params['sign'] = self.create_sign_key(params)
        data = {
            'name': 'Pay',
            'method': 'POST',
            'action': 'https://pay.piastrix.com/ru/pay',
            'fields': params,
        }
        return render_template('payment_form.html', data=data, form=None)


class UsdStrate(AbstractStrategy):
    def __init__(self):
        self._required_fields = sorted({'shop_amount', 'shop_currency', 'shop_id', 'shop_order_id', 'payer_currency', })
        self._url = Config.USD_URL

    def execute(self, params=None):
        # send request and show response
        params.update({"shop_amount": params.get('amount', 0),
                       "shop_currency": 840,
                       "payer_currency": 840,
                       })
        print(f"Params: {params}")
        params['sign'] = self.create_sign_key(params)
        r = requests.post(self._url, json=params)
        if r.status_code == 200:
            try:
                data = r.json()
            except json.JSONDecodeError:
                data = re.sub(r'"url": (https?.*?)\s.*?}', r'"url":  "\1" },', r.text)  # url value has not "
                data = json.loads(data)
            print(f"DATA: {data}")
            if data['result']:
                return redirect(data['data']['url'])
            else:
                return redirect(url_for('index'))
        else:
            print('Error with requsts, code: ', r.status_code)
            raise False


class RubStrate(AbstractStrategy):
    def __init__(self):
        self._required_fields = sorted({'amount', 'currency', 'payway', 'shop_id', 'shop_order_id', })
        self._url = Config.RUB_URL

    def execute(self, params=None):
        # send requests and from response create html form
        params.update({"currency": 643, "payway": "payeer_rub",})
        print(f"Params: {params}")
        params['sign'] = self.create_sign_key(params)
        r = requests.post(self._url, json=params)
        if r.status_code == 200:
            data = r.json()
            flash(f"DATA: {data}")
            if data['result']:
                res = {
                    'name': 'Pay',
                    'method': data['data']['method'],
                    'action': data['data']['url'],
                    'fields': data['data']['data'],
                }
                return render_template('payment_form.html', data=res, form=None)
            else:
                print('Error with data:', data)
                return redirect(url_for('index'))
        else:
            print('Error with requsts, code: ', r.status_code)
            raise False


def choose_strategy(currency):
    currencies = {
        'eur': EuroStrate,
        'usd': UsdStrate,
        'rub': RubStrate,
    }
    return currencies[currency]()
