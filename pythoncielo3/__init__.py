# -*- coding: utf-8 -*-

# Standart libs
from random import randint
from copy import deepcopy
from json import dumps

# Related third party libs
from requests import post

__all__ = ['Transaction']

_DEFAULT_TRANSACTION = {
    'MerchantOrderId': None,
    'Customer': {
        'Name': None,
    },
    'Payment': {
        'Type': 'CreditCard',
        'Amount': None,
        'Installments': 1,
        'CreditCard': {
            'CardNumber': None,
            'Holder': None,
            'ExpirationDate': None,
            'SecurityCode': None,
            'Brand': None
        }
    }
}


class Transaction(object):
    def __init__(self, merchant_id, merchant_key, sandbox=False):
        def get_write_url():
            if sandbox:
                return 'https://apisandbox.cieloeCommerce.cielo.com.br/'

            else:
                return 'https://api.cieloeCommerce.cielo.com.br/'

        self._data = deepcopy(_DEFAULT_TRANSACTION)
        self._merchant_id = merchant_id
        self._merchant_key = merchant_key
        self._api_write_url = get_write_url()
        self.request_id = str(randint(1, 99999999999))
        self._data['Payment']['Provider'] = 'Simulado' if sandbox else 'Cielo'

    def _to_camel_case(self, snake_case):
        return ''.join(x.title() for x in snake_case.split('_'))

    def _make_header(self):
        return {
            'MerchantId':  self._merchant_id,
            'MerchantKey':  self._merchant_key,
            'RequestId':  self.request_id,
            'Content-Type':  'application/json'
        }

    def set_customer(self, **customer):
        self._data['Customer'] = {}

        for key, val in customer.items():
            self._data['Customer'][self._to_camel_case(key)] = val

    def set_credit_card(self, **card):
        self._data['Payment']['CreditCard'] = {}

        for key, val in card.items():
            self._data['Payment']['CreditCard'][self._to_camel_case(key)] = val

    def __setattr__(self, name, value):
        editable_payment_fields = [
            'amount', 'currency', 'country', 'service_tax_amount',
            'installments', 'interest', 'authenticate'
        ]

        if name in ['merchant_order_id', 'customer', 'payment']:
            self._data[self._to_camel_case(name)] = value

        elif name in editable_payment_fields:
            self._data['Payment'][self._to_camel_case(name)] = value

        else:
            super(Transaction, self).__setattr__(name, value)

    def create(self, capture=False):
        def was_authorized():
            if res.status_code == 201:
                return 'AuthorizationCode' in raw.get('Payment', {})

            return False

        self._data['Payment']['Capture'] = capture

        url = '%s/1/sales/' % self._api_write_url
        res = post(url, dumps(self._data), headers=self._make_header())
        raw = res.json()

        return {'success': was_authorized(), 'raw': raw}
