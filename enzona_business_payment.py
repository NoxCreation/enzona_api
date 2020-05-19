'''
This library is still in the process of being created. It is not recommended to use it yet in development.

Author: Josué Carballo Baños
License: GNU GPL from the Free Software Foundation v3 and later.
'''

import json
import requests

import enzona_api


class enzona_business_payment(enzona_api):

    def __init__(self, consumer_key, consumer_secret):
        """
        Initiates entry to the system with the private and secret keys
        :param consumer_key: Private key granted
        :param consumer_secret: Public key granted
        """
        enzona_api.__init__(self, consumer_key, consumer_secret)

    def create_payments(self, payment):
        """
        Allows you to create a payment
        :param payment: Payment object with all payment data
        :return: Return object Json with payment data
        """
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {0}".format(self.token)
        }
        response = requests.post("https://api.enzona.net/payment/v1.0.0/payments", data= json.dumps(payment), headers=headers)
        print(response.text)
        return response.json()

    def cancel_payments(self, transaction_uuid):
        """
        Allows you to cancel a payment
        :param transaction_uuid: Transaction Identifier
        :return: Returns json object with cancellation data
        """
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {0}".format(self.token)
        }
        response = requests.post("https://api.enzona.net/payment/v1.0.0/payments/{0}/cancel".format(transaction_uuid), headers=headers)
        return response.json()

    #Completar un pago
    def complete_payments(self, transaction_uuid):
        """
        Allows you to complete a payment
        :param transaction_uuid: Transaction Identifier
        :return: Returns json object with completed data
        """
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {0}".format(self.token)
        }
        data = {}
        response = requests.post("https://api.enzona.net/payment/v1.0.0/payments/{0}/complete".format(transaction_uuid),data=data, headers=headers)
        return response.json()

    def get_payments(self, merchant_uuid, offset, limit, status_filter = None, start_date_filter=None, end_date_filter=None):
        """
        You get a list of payments made
        :param merchant_uuid: Business Identifier
        :param offset: Where to start showing the data
        :param limit: Amount of data to be displayed
        :param status_filter: Payment status
        :return: Return you get a list of payments made
        """
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {0}".format(self.token)
        }
        if status_filter != None:
            status_filter = "&status_filter="+str(status_filter)
        else:
            status_filter = ""
        response = requests.get("https://api.enzona.net/payment/v1.0.0/payments?"+
                                "merchant_uuid="+merchant_uuid+
                                "&limit="+str(limit)+
                                "&offset="+str(offset)+
                                "&order_filter=desc"+status_filter+
                                "&start_date_filter="+start_date_filter+
                                "&end_date_filter="+end_date_filter
                                , headers=headers)
        return response.json()

    def payments_refund(self, merchant_uuid, offset, limit, status_filter = None):
        """
        You get a list of returns made
        :param merchant_uuid: Business Identifier
        :param offset: Where to start showing the data
        :param limit: Amount of data to be displayed
        :param status_filter: Payment status
        :return: Return you get a list of returns made
        """
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {0}".format(self.token)
        }
        if status_filter != None:
            status_filter = "&status_filter="+str(status_filter)
        else:
            status_filter = ""
        response = requests.get("https://api.enzona.net/payment/v1.0.0/payments/refunds?merchant_uuid=" + merchant_uuid +"&limit="+str(limit)+"&offset=" + str(offset) +"&order_filter=desc"+status_filter, headers=headers)
        return response.json()

class Payments():

    def __init__(self,
                 description_payment,
                 description_product,
                 title, currency, shipping,
                 tax, discount, tip, price,
                 merchant_op_id,
                 invoice_number,
                 return_url, cancel_url ,
                 terminal_id):
        price = str(price)
        total = str( round( (float(shipping) + float(tax) + float(price) - float(discount)) *100 ) / 100)

        if len(total.split(".")[1]) < 2:
            total += "0"
        if len(price.split(".")[1]) < 2:
            price += "0"
        if len(shipping.split(".")[1]) < 2:
            shipping += "0"
        if len(tax.split(".")[1]) < 2:
            tax += "0"

        self.payment_data = {
            "description": description_payment,
            "currency": currency,
            "amount": {
                "total": str(total),
                "details": {
                    "shipping": shipping,
                    "tax": tax,
                    "discount": discount,
                    "tip": tip
                }
            },
            "items": [
                {
                    "name": title,
                    "description": description_product,
                    "quantity": 1,
                    "price": price,
                    "tax": tax
                }
            ],
            "merchant_op_id": merchant_op_id,
            "invoice_number": invoice_number,
            "return_url": return_url,
            "cancel_url": cancel_url,
            "terminal_id": terminal_id,
            "buyer_identity_code": ""
        }

    def get_payment(self):
        return self.payment_data