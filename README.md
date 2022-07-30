# Enzona_api
This library is still in the process of being created. It is not recommended to use it yet in development. The **PaymentAPI** and **QRAPI** development process will be incorporated gradually.

Enzona's payment platform API access library (https://www.enzona.net/)

# How to install?

    pip install enzona-api
 
 Requires Python >= 3.5 with pip. (https://pypi.org/project/enzona-api/)

# Acquiring the access keys
To acquire the credentials to use this platform you must register your business at https://bulevar.enzona.net/. Once you have registered your business, to make the corresponding API requests you must access https://api.enzona.net/store/. The credentials for access to the above system, must be sent to your email within 72 hours (At the time of this publication, the granting of credentials was paralyzed but will be continued thereafter). Authenticated you must check if the registered commerce appears from the **Applications** section:

![screenshot1](https://github.com/JosueCarballo/enzona_api/blob/master/screenshot/enzona_api_aplicaciones1.png)

We enter our shop and in **Production Keys** we notice that we have two keys, **Consumer Key** and the **Consumer Secret**. Both keys must be copied in order to use the enzyme_api library.

![screenshot2](https://github.com/JosueCarballo/enzona_api/blob/master/screenshot/enzona_api_keys.png)

# Create a payment
    from enzona_api.enzona_business_payment import enzona_business_payment
    
    ebp = enzona_business_payment(CONSUMER_KEY, CONSUMER_SECRET)
    
    merchant_uuid = "her put your merchant_uuid" #your merchant_uuid
    
    SHIPPING = 10.0
    DISCOUNT = 2.0
    TIP = 5.0
    MERCHANT_OP_ID = 950201146651 #your market identifier
    INVOICE_NUMBER = 1004 #invoice number
    TERMINAL_ID = 12121 #terminal identifier (POS, Cash Register, etc.)
    URL_RETURN = "http://www.example.com/return_payment"
    URL_CANCEL = "http://www.example.com/cancel_payment"
    
    product1 = Product(name="producto1", description="description1", quantity=1, price=403.5, tax=20.18)
    product2 = Product(name="producto2", description="description2", quantity=2, price=300.0, tax=15.0)
    lst_products = [product1.get_product(), product2.get_product()]
    
    pay = Payments(
        merchant_uuid=merchant_uuid,
        description_payment= "Description pay",
        currency="CUP",
        shipping=SHIPPING,
        discount=DISCOUNT,
        tip=TIP,
        lst_products=lst_products,
        merchant_op_id=MERCHANT_OP_ID,
        invoice_number=INVOICE_NUMBER,
        return_url=URL_RETURN,
        cancel_url=URL_CANCEL,
        terminal_id=TERMINAL_ID
    )
    
    response = ebp.create_payments(payment=pay.get_payment())
    transaction_uuid = response.transaction_uuid()
    link_confirm = response.link_confirm()
    
The function create_payments returns an object of type response_payments with the following functionalities
- **transaction_uuid**: Transaction identifier
- **link_confirm**: A redirection link to the client who is making the payment to the Enzona platform for confirmation and payment.

![screenshot3](https://github.com/JosueCarballo/enzona_api/blob/master/screenshot/pago_enzona_web.png)

The url value set in **URL_RETURN** corresponds to the url that will redirect Enzona once the platform is successfully completed. **URL_CANCEL** is the url in case of cancellation. 

# Confirmation of a payment
In case of an effective payment you must make a confirmation of the payment:

    response = ebp.complete_payments(transaction_uuid=transaction_uuid)
    print(response.transaction_uuid())
    print(response.status_denom())
    
When a successful payment is made from the platform, it returns to URL_RETURN with a transaction_uuid value in its GET request:

Example: www.example.com/complete_payment?transaction_uuid=eff02133c1724287b10860824c596777

That value must be captured and the payment confirmation created. The complete_payments function returns an object of type response_operation_payments:
- **transaction_uuid**: Transaction identifier
- **status_denom**: Status name of the transaction

# Cancel the payment
In case of cancellation of a payment:

    response = ebp.cancel_payments(transaction_uuid=transaction_uuid)
    print(response.transaction_uuid())
    print(response.status_denom())
    
The function cancel_payments returns a response_operation_payments object and cancels the initiated payment.

# Refund of payments
To make a partial payment you must use the payments_refund function with the Payload parameter that indicates the value you want to return to the customer. Not using this parameter indicates that a full payment has been made:

    #Pago parcial
    payload = Payload(total=20.0, description="devolucion parcial1")
    response = ebp.payments_refund(transaction_uuid="57c5c848b00743db922022c92ad1d24f", Payload=payload)
    print(response.transaction_uuid())
    print(response.created_at())
    print(response.amount_total())
    print(response.description())
    print(response.refund_fullname())
    
    #Pago total
    response = ebp.payments_refund(transaction_uuid="57c5c848b00743db922022c92ad1d24f")
    print(response.transaction_uuid())
    print(response.created_at())
    print(response.amount_total())
    print(response.description())
    print(response.refund_fullname())

The payments_refund function returns a response_refound type object with the following functionality:
- **transaction_uuid**: Transaction identifier
- **created_at**: Date of return
- **amount_total**: Total returned
- **description**: Description given for the return
- **refund_fullname**: Full name of the customer to whom the return is made.

# Get payments made
To obtain all the payments made, you must use the get_payments function, which returns a list of the payment data. This has several parameters:

- **merchant_uuid**: Merchant Identifier
- **offset**: Where to start displaying the data (Default 0)
- **limit**: Amount of data to be displayed (Default 10)
- **status_filter**: Filter by payment status
    - **1112**: Failure
    - **1116**: Confirmed
    - **1111**: Accepted
- **start_date_filter**: Initial date for filtering payments
- **end_date_filter**: Final date for filtering payments

        payments = ebp.get_payments(merchant_uuid=merchant_uuid)
        for payment in payments.get_payments():
            print(payment.invoice_number())
            print(payment.amount_total())
            print(payment.amount_tip())
            print(payment.amount_discount())
            print(payment.amount_shipping())
            print(payment.amount_tax())
            print(payment.status_denom())
            print(payment.commission())
            print("")

In order to know the merchant_uid of your market you must enter the Enzona platform in the merchant section (https://www.enzona.net/merchant) and in the list of your merchants press Details of your market and a series of information will appear that you introduced during the creation of the trade. The merchant_uuid is the market ID.

![screenshot4](https://github.com/JosueCarballo/enzona_api/blob/master/screenshot/comercios.png)

# Get refound made
To obtain the returns made you use the function get_payments_refund that will return an object of type response_get_refound that is a list of the return operations:

    response = ebp.get_payments_refund(merchant_uuid=merchant_uuid)
    refunds = response.get_refunds()
    for refund in refunds:
        print(refund["transaction_uuid"])
        print(refund["refund_fullname"])
        print(refund["refunded"])
        print(refund["total_refunded"])
        print(refund["total"])
        print("")

# Thanks to
- Alejandro Lavin (Developer Enzona)
- Sergio Miguel Damas Milán (Developer Enzona)
- Carlos Cesar Caballero (Developer)
- Dennis Beltrán Romero (Collaborator)

# Source
- https://apisandbox.enzona.net/store/site/themes/wso2/templates/api/documentation/download.jag?tenant=carbon.super&resourceUrl=/registry/resource/_system/governance/apimgt/applicationdata/provider/admin/PaymentAPI/v1.0.0/documentation/files/C%C3%B3mo%20Obtener%20el%20token%20de%20acceso%20en%20las%20%20APIs.docx
- https://apisandbox.enzona.net/store/site/themes/wso2/templates/api/documentation/download.jag?tenant=carbon.super&resourceUrl=/registry/resource/_system/governance/apimgt/applicationdata/provider/admin/PaymentAPI/v1.0.0/documentation/files/Documentaci%C3%B3n%20de%20la%20API%20de%20Payment.docx
- http://enzonatuto.intellifoundry.com/?fbclid=IwAR2_-5-en2liC64HRyNNkc7DxJ1jpZimnlXciZC6vbgv_Ghe8Va5fBVApsk




