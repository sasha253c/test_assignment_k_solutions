import json
import re
import hashlib
from abc import ABC, abstractmethod

import requests
from flask import render_template, flash, redirect, url_for

from app import app
from app.logger import function_logger
from config import DevelopmentConfig as Config


class AbstractStrategy(ABC):
    def __init__(self):
        self._required_fields = tuple()
        self.params = {}

    @abstractmethod
    def execute(self, params=None):
        if params is None:
            self.params = {}
        else:
            self.params = params.copy()

    def create_sign_key(self, params):
        assert params.keys() >= set(self._required_fields)
        s = ':'.join(str(params.get(k, '')) for k in self._required_fields) + Config.SECRET
        m = hashlib.sha256()
        m.update(s.encode())
        return m.hexdigest()


class EuroStrategy(AbstractStrategy):
    def __init__(self):
        self._required_fields = sorted({'amount', 'currency', 'shop_id', 'shop_order_id'})

    @function_logger
    def execute(self, params=None):
        super().execute(params)
        self.params.update({'currency': 978})
        print(f"Params: {self.params}")
        self.params['sign'] = self.create_sign_key(self.params)
        data = {
            'name': 'Pay',
            'method': 'POST',
            'action': 'https://pay.piastrix.com/ru/pay',
            'fields': self.params,
        }
        return render_template('payment_form.html', data=data, form=None)


class UsdStrategy(AbstractStrategy):
    def __init__(self):
        self._required_fields = sorted({'shop_amount', 'shop_currency', 'shop_id', 'shop_order_id', 'payer_currency', })
        self._url = Config.USD_URL

    @function_logger
    def execute(self, params=None):
        super().execute(params)
        self.params.update({"shop_amount": self.params.get('amount', 0),
                       "shop_currency": 840,
                       "payer_currency": 840,
                       })
        print(f"Params: {self.params}")
        self.params['sign'] = self.create_sign_key(self.params)
        r = requests.post(self._url, json=self.params)
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
            app.logger.warning(f"Status code to {self._url} != 200, params: {self.params}")


class RubStrategy(AbstractStrategy):
    def __init__(self):
        self._required_fields = sorted({'amount', 'currency', 'payway', 'shop_id', 'shop_order_id', })
        self._url = Config.RUB_URL

    @function_logger
    def execute(self, params=None):
        super().execute(params)
        self.params.update({"currency": 643, "payway": "payeer_rub",})
        print(f"Params: {self.params}")
        self.params['sign'] = self.create_sign_key(self.params)
        r = requests.post(self._url, json=self.params)
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
                app.logger.warning(f'Not found result: {data}')
                return redirect(url_for('index'))
        else:
            app.logger.warning(f"Status code to {self._url} != 200, params: {self.params}")


def choose_strategy(currency):
    currencies = {
        'eur': EuroStrategy,
        'usd': UsdStrategy,
        'rub': RubStrategy,
    }
    return currencies[currency]()
