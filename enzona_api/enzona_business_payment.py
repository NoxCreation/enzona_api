"""
This library is still in the process of being created. It is not recommended
to use it yet in development.

Author: Josué Carballo Baños
License: GNU GPL from the Free Software Foundation v3 and later.
"""

import json
import requests

from enzona_api import enzona_api
from enzona_api.responses import response_payments, \
    response_operation_payments, response_return_payments, response_refound, \
    response_get_refound
from enzona_api.error import EnzonaError


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
        response = requests.post(
            "https://api.enzona.net/payment/v1.0.0/payments",
            data=json.dumps(payment), headers=headers)
        try:
            if response.status_code != 200:
                return {
                    "error": response.reason,
                    "code": response.status_code,
                    "url": response.url,
                    "headers": response.headers,
                }
            else:
                return response_payments(response.json())
        except EnzonaError as e:
            print(e)
            return e

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
        response = requests.post(
            "https://api.enzona.net/payment/v1.0.0/payments/{0}/cancel".format(
                transaction_uuid), headers=headers)
        try:
            if response.status_code != 200:
                return {
                    "error": response.reason,
                    "code": response.status_code,
                    "url": response.url,
                    "headers": response.headers,
                }
            else:
                return response_operation_payments(response.json())
        except EnzonaError as e:
            print(e)
            return e

    # Completar un pago
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
        response = requests.post(
            "https://api.enzona.net/payment/v1.0.0/payments/{0}/"
            "complete".format(transaction_uuid), data=data, headers=headers)
        try:
            if response.status_code != 200:
                return {
                    "error": response.reason,
                    "code": response.status_code,
                    "url": response.url,
                    "headers": response.headers,
                }
            else:
                return response_operation_payments(response.json())
        except EnzonaError as e:
            print(e)
            return e

    def get_payments(self, merchant_uuid, offset=0, limit=10,
                     status_filter=None, start_date_filter="",
                     end_date_filter=""):
        """
        You get a list of payments made
        :param end_date_filter:
        :param start_date_filter:
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
        if status_filter is not None:
            status_filter = "&status_filter=" + str(status_filter)
        else:
            status_filter = ""
        response = requests.get(
            "https://api.enzona.net/payment/v1.0.0/payments?" +
            "merchant_uuid=" + merchant_uuid +
            "&limit=" + str(limit) +
            "&offset=" + str(offset) +
            "&order_filter=desc" + status_filter +
            "&start_date_filter=" + start_date_filter +
            "&end_date_filter=" + end_date_filter, headers=headers)
        try:
            if response.status_code != 200:
                return {
                    "error": response.reason,
                    "code": response.status_code,
                    "url": response.url,
                    "headers": response.headers,
                }
            else:
                return response_return_payments(response.json())
        except EnzonaError as e:
            print(e)
            return e

    def payments_refund(self, transaction_uuid, Payload=None):
        """
        :param transaction_uuid: Transaction Identifier
        :param Payload: (Optional) Partial return structure
        :return: Returns the data of the refund transaction
        """
        headers = {
            'Content-Type': 'application/json',
            "Authorization": "Bearer {0}".format(self.token)
        }
        if Payload is None:
            payload = {}
        else:
            payload = Payload.get_payload()
        try:
            response = requests.post(
                "https://api.enzona.net/payment/v1.0.0/payments/" +
                transaction_uuid + "/refund",
                data=json.dumps(payload), headers=headers)
            return response_refound(response.json())
        except EnzonaError as e:
            print(e)
            return e

    def get_payments_refund(self, merchant_uuid, offset=0, limit=10,
                            status_filter=None):
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
        if status_filter is not None:
            status_filter = "&status_filter=" + str(status_filter)
        else:
            status_filter = ""
        response = requests.get(
            "https://api.enzona.net/payment/v1.0.0/payments/refunds?"
            "merchant_uuid=" + merchant_uuid + "&limit=" + str(
                limit) + "&offset=" + str(
                offset) + "&order_filter=desc" + status_filter,
            headers=headers)
        try:
            return response_get_refound(response.json())
        except EnzonaError as e:
            print(e)
            return e


class Payload():
    def __init__(self, total, description):
        self.total = total
        self.description = description

    def get_payload(self):
        if len(str(self.total).split(".")[1]) < 2:
            total = str(self.total) + "0"
        else:
            total = self.total
        return {
            "amount": {
                "total": total
            },
            "description": self.description
        }


class mProduct():
    def __init__(self, name, description, quantity, price, tax):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.price = float(price)
        self.tax = float(tax)

    def get_product(self):
        if len(str(self.price).split(".")[1]) < 2:
            price = str(self.price) + "0"
        else:
            price = str(self.price)
        if len(str(self.tax).split(".")[1]) < 2:
            tax = str(self.tax) + "0"
        else:
            tax = str(self.tax)
        return {"name": self.name, "description": self.description,
                "quantity": self.quantity, "price": price, "tax": tax}


class Payments():
    def __init__(self, merchant_uuid, description_payment, currency, shipping,
                 discount, tip, lst_products, merchant_op_id, invoice_number,
                 return_url, cancel_url, terminal_id):

        shipping = float(shipping)
        discount = float(discount)
        tip = float(tip)
        total_price = 0
        for product in lst_products:
            total_price += float(product["quantity"]) * float(product["price"])
        total_tax = 0
        for product in lst_products:
            total_tax += float(product["tax"])

        total_pay = str(round((shipping + total_tax + total_price + (
                    tip - discount)) * 100) / 100)

        if len(str(total_pay).split(".")[1]) < 2:
            total_pay = str(total_pay) + "0"
        else:
            total_pay = str(total_pay)
        if len(str(total_tax).split(".")[1]) < 2:
            total_tax = str(total_tax) + "0"
        else:
            total_tax = str(total_tax)
        if len(str(shipping).split(".")[1]) < 2:
            shipping = str(shipping) + "0"
        else:
            shipping = str(shipping)
        if len(str(discount).split(".")[1]) < 2:
            discount = str(discount) + "0"
        else:
            discount = str(discount)
        if len(str(tip).split(".")[1]) < 2:
            tip = str(tip) + "0"
        else:
            tip = str(tip)

        self.payment_data = {
            "merchant_uuid": merchant_uuid,
            "description": description_payment,
            "currency": currency,
            "amount": {
                "total": str(total_pay),
                "details": {
                    "shipping": shipping,
                    "tax": total_tax,
                    "discount": discount,
                    "tip": tip
                }
            },
            "items": lst_products,
            "merchant_op_id": merchant_op_id,
            "invoice_number": str(invoice_number),
            "return_url": return_url,
            "cancel_url": cancel_url,
            "terminal_id": terminal_id,
            "buyer_identity_code": ""
        }

    def get_payment(self):
        return self.payment_data
