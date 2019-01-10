import os
import sys
import requests
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app


class TestPaymentForm(unittest.TestCase):
    FIELDS = ("amount", "currency", "shop_id", "shop_order_id", "description", "submit",)

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def test_main_page(self):
        with app.test_client() as c:
            response = c.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_field_exists(self):
        with app.test_client() as c:
            response = c.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            html = response.data.decode("utf-8")
            for field in self.FIELDS:
                self.assertRegex(html, rf'''<(?:input|select|textarea).*?id=['"]{field}['"].*?>''')

    def test_invalid_form(self):
        self.invalid_amount()
        self.invalid_currency()

    def invalid_amount(self):
        for amount in (-1, -10, 'amount', None,):
            html = self.send_payment_form({'amount': amount})
            self.assertRegex(html,
                             r'''<p.*?class=['"]help-block['"].*?>(?:This field is required|Number must be at least 0)\.</p>''')

    def invalid_currency(self):
        for currency in (10, 'invalid_currency',):
            html = self.send_payment_form({'amount': 1, 'currency': currency})
            self.assertRegex(html, r'''<p.*?class=['"]help-block['"].*?>Not a valid choice</p>''')

    def send_payment_form(self, data):
        with app.test_client() as c:
            response = c.post('/', data=data, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            return response.data.decode('utf-8').replace('\n', '')

    def test_eur_currency(self):
        data = {'amount': 1, 'currency': 'eur', 'shop_id': 5, 'shop_order_id': 15}
        html = self.send_payment_form(data)

        self.assertRegex(html, r'''<form.*?name=['"]Pay['"].*?>''')
        self.assertRegex(html, r'''<form.*?method=['"]POST['"].*?>''')
        self.assertRegex(html, r'''<form.*?action=['"]https://pay.piastrix.com/ru/pay['"].*?>''')
        for name, value in data.items():
            if name == 'currency':
                value = 978
            self.assertRegex(html, rf'''<input.*?name=['"]{name}['"].*?>''')
            self.assertRegex(html, rf'''<input.*?value=['"]{value}['"].*?>''')

    def test_usd_currency(self):
        data = {'amount': 1, 'currency': 'usd', 'shop_id': 5, 'shop_order_id': 15}
        # Fixme: Redirect to another server
        with self.assertRaises(RuntimeError):
            self.send_payment_form(data)

    def test_rub_currency(self):
        values = {
            "currency": "643",
            "payway": "card_rub",
            "amount": "12.34",
            "shop_id": 112,
            "shop_order_id": 4129,
            "description": "Test invoice",
            "sign": "8fb2cafda4da9de1f1c00787dd5d22e6a8094256d0e47b633783f652624b81d4",
        }
        headers = {
            'Content-Type': 'application/json',
        }
        r = requests.post(app.config.get('RUB_URL'), data=values, headers=headers)
        response_data = r.json()
        self.assertTrue(response_data['result'])
        self.assertEqual(response_data['message'], 'Ok')

        data = {'amount': 1, 'currency': 'rub', 'shop_id': 5, 'shop_order_id': 15}
        html = self.send_payment_form(data)

        self.assertIn(response_data['data']['method'], html)
        self.assertIn(response_data['data']['url'], html)
        for name, value in response_data['data']['data'].items():
            self.assertRegex(html, rf'''<input.*?name=['"]{name}['"].*?>''')
            self.assertRegex(html, rf'''<input.*?value=['"]{value}['"].*?>''')


if __name__ == '__main__':
    unittest.main()
