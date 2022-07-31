from enzona_api.error import EnzonaError


class response_payments():
    def __init__(self, response):
        self.response = response

    def transaction_uuid(self):
        try:
            return self.response['transaction_uuid']
        except:
            raise EnzonaError(self.response['fault']['message'])

    def link_confirm(self):
        try:
            return self.response['links'][0]['href']
        except:
            raise EnzonaError(self.response['fault']['message'])

    def link_complete(self):
        try:
            return self.response['links'][1]['href']
        except:
            raise EnzonaError(self.response['fault']['message'])

    def link_cancel(self):
        try:
            return self.response['links'][2]['href']
        except:
            raise EnzonaError(self.response['fault']['message'])


class response_operation_payments():
    def __init__(self, response):
        self.response = response

    def transaction_uuid(self):
        try:
            return self.response['transaction_uuid']
        except:
            raise EnzonaError(self.response['fault']['message'])

    def status_denom(self):
        try:
            return self.response['status_denom'][0]
        except:
            raise EnzonaError(self.response['fault']['message'])


class response_return_payments():
    def __init__(self, response):
        self.response = response

    def get_payments(self):
        payments = self.response['payments']
        lst_payments = []
        for mpayment in payments:
            lst_payments.append(self.payment(mpayment))
        return lst_payments

    class payment():
        def __init__(self, response): self.response = response

        def invoice_number(self): return self.response['invoice_number']

        def amount_total(self): return self.response['amount']['total']

        def amount_tip(self): return self.response['amount']['details']['tip']

        def amount_discount(self): return self.response['amount']['details'][
            'discount']

        def amount_shipping(self): return self.response['amount']['details'][
            'shipping']

        def amount_tax(self): return self.response['amount']['details']['tax']

        def status_denom(self): return self.response['status_denom']

        def commission(self): return self.response['commission']


class response_refound():
    def __init__(self, response):
        self.response = response

    def transaction_uuid(self):
        try:
            return self.response['transaction_uuid']
        except:
            raise EnzonaError(self.response['fault']['message'])

    def created_at(self):
        try:
            return self.response['created_at']
        except:
            raise EnzonaError(self.response['fault']['message'])

    def amount_total(self):
        try:
            return self.response['amount']['total']
        except:
            raise EnzonaError(self.response['fault']['message'])

    def description(self):
        try:
            return self.response['description']
        except:
            raise EnzonaError(self.response['fault']['message'])

    def refund_fullname(self):
        try:
            return self.response['refund_name'] + ' ' + self.response[
                'refund_lastname']
        except:
            raise EnzonaError(self.response['fault']['message'])


class response_get_refound():
    def __init__(self, response):
        self.response = response

    def get_refunds(self):
        refunds = self.response['refunds']
        lst_refunds = []
        for refund in refunds:
            lst_refunds.append({
                'transaction_uuid': refund['transaction_uuid'],
                'transaction_denom': refund['transaction_denom'],
                'status_denom': refund['status_denom'],
                'transaction_created_at': refund['transaction_created_at'],
                'refund_avatar': refund['refund_avatar'],
                'refund_fullname': refund['name'] + ' ' + refund['lastname'],
                'refunded': refund['amount']['details']['refunded'],
                'total_refunded': refund['amount']['details'][
                    'total_refunded'],
                'total': refund['amount']['total'],
            })
        return lst_refunds
