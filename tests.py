import unittest

from pythoncielo3 import Transaction

_MERCHANT_ID = '499b1bc7-8783-4b5d-8d42-f738fb68a848'
_MERCHANT_KEY = 'UYONWSYAYBAYWLERUJUGHIWCMYYBISWHBHUBMIEB'


class TestSandbox(unittest.TestCase):
    def setUp(self):
        self.trans = Transaction(_MERCHANT_ID, _MERCHANT_KEY, sandbox=True)

    def test_create_empty_transaction(self):
        res = self.trans.create()
        errors = [e['Code'] for e in res['raw']]

        self.assertFalse(res['success'])
        self.assertIn(105, errors)  # Customer Name is required.
        self.assertIn(122, errors)  # MerchantOrderId is required.

    def test_create_basic_transaction(self):
        self.trans.merchant_order_id = '0001'
        self.trans.amount = 10000
        self.trans.set_customer(name='Pedro Costa')
        self.trans.set_credit_card(card_number='0000000000000001',
                                   holder='Pedro Costa', security_code='123',
                                   expiration_date='12/2099', brand='Visa')

        res = self.trans.create()
        card = res['raw']['Payment']['CreditCard']

        self.assertTrue(res['success'])
        self.assertEqual(res['raw']['MerchantOrderId'], '0001')
        self.assertEqual(res['raw']['Customer']['Name'], 'Pedro Costa')
        self.assertEqual(res['raw']['Payment']['Amount'], 10000)
        self.assertFalse(res['raw']['Payment']['Capture'])
        self.assertEqual(card['CardNumber'], '000000******0001')
        self.assertEqual(card['Holder'], 'Pedro Costa')
        self.assertEqual(card['ExpirationDate'], '12/2099')
        self.assertEqual(card['Brand'], 'Visa')
        self.assertFalse(card['SaveCard'])

    def test_create_copletetransaction(self):
        cli = {
            'name': 'Pedro Costa',
            'email': 'pedro@costa.com',
            'birthdate': '1991-01-02',
            'address': {
                'Street': 'Rua Teste',
                'Number': '123',
                'Complement': 'AP 123',
                'ZipCode': '12345987',
                'City': 'Rio de Janeiro',
                'State': 'RJ',
                'Country': 'BRA'
            },
            'delivery_address': {
                'Street': 'Rua Teste',
                'Number': '123',
                'Complement': 'AP 123',
                'ZipCode': '12345987',
                'City': 'Rio de Janeiro',
                'State': 'RJ',
                'Country': 'BRA'
            }
        }
        self.trans.set_customer(**cli)
        self.trans.set_credit_card(card_number='0000000000000001',
                                   holder='Pedro Costa', security_code='123',
                                   expiration_date='12/2099', brand='Visa')
        self.trans.merchant_order_id = '0001'
        self.trans.amount = 10000
        self.trans.installments = 2

        res = self.trans.create(capture=True)
        card = res['raw']['Payment']['CreditCard']

        self.assertTrue(res['success'])
        self.assertEqual(res['raw']['MerchantOrderId'], '0001')
        self.assertEqual(res['raw']['Customer']['Name'], cli['name'])
        self.assertEqual(res['raw']['Customer']['Email'], cli['email'])
        self.assertEqual(res['raw']['Customer']['Birthdate'], cli['birthdate'])
        self.assertEqual(res['raw']['Customer']['Address'], cli['address'])
        self.assertEqual(res['raw']['Customer']['DeliveryAddress'],
                         cli['delivery_address'])
        self.assertEqual(res['raw']['Payment']['Amount'], 10000)
        self.assertEqual(res['raw']['Payment']['Installments'], 2)
        self.assertTrue(res['raw']['Payment']['Capture'])
        self.assertEqual(card['CardNumber'], '000000******0001')
        self.assertEqual(card['Holder'], 'Pedro Costa')
        self.assertEqual(card['ExpirationDate'], '12/2099')
        self.assertEqual(card['Brand'], 'Visa')
        self.assertFalse(card['SaveCard'])

    def test_create_unauthorized_transaction(self):
        self.trans.merchant_order_id = '0001'
        self.trans.amount = 10000
        self.trans.set_customer(name='Pedro Costa')
        self.trans.set_credit_card(card_number='0000000000000002',
                                   holder='Pedro Costa', security_code='123',
                                   expiration_date='12/2099', brand='Visa')

        res = self.trans.create()

        self.assertFalse(res['success'])

if __name__ == '__main__':
    unittest.main()
