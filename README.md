# Python Cielo API 3.0

Integração **simplificada** do python com a [API 3.0 da Cielo](http://developercielo.github.io/Webservice-3.0/).
A integração permite compra com cartão de crédito e personalização de captura
automática, número de parcelas, etc.

## Criando e capturando uma compra com cartão de crédito
```python
    from cielo import Transaction

    # Os valores abaixo são informados pela Cielo. As chaves do ambiente de teste
    # podem ser obtidas em: https://cadastrosandbox.cieloecommerce.cielo.com.br
    merchant_id = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
    merchant_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    # Para fazer transação fora do ambiente de testes remova sandbox=True da
    # chamada abaixo.
    trans = Transaction(merchant_id, merchant_key, sandbox=True)

    trans.merchant_order_id = '0001'
    trans.amount = 10000
    trans.set_customer(name='Pedro Costa')
    trans.set_credit_card(card_number='0000000000000001', holder='Pedro Costa',
                          security_code='123', expiration_date='12/2021',
                          brand='Visa')

    res = trans.create(capture=True)

    print(res['success'])
    print(res['raw']['Payment']['Tid'])
```

## Instalação

```
git clone https://github.com/eduardomb/pythoncielo3
pip install -r pythoncielo3/requirements.txt
```

## Disclaimer

* A integração não permite fazer operações de leitura na API da cielo.
* Apenas foram testadas compras com cartão de crédito.
* O código foi testado apenas com python `3.5.1`.
