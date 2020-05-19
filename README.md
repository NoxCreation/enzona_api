# enzona_api
This library is still in the process of being created. It is not recommended to use it yet in development. The **PaymentAPI** and **QRAPI** development process will be incorporated gradually.

Enzona's payment platform API access library (https://www.enzona.net/)

# Acquiring the access keys
To acquire the credentials to use this platform you must register your business at https://bulevar.enzona.net/. Once you have registered your business, to make the corresponding API requests you must access https://api.enzona.net/store/. The credentials for access to the above system, must be sent to your email within 72 hours (At the time of this publication, the granting of credentials was paralyzed but will be continued thereafter). Authenticated you must check if the registered commerce appears from the **Applications** section:

![screenshot1](https://github.com/JosueCarballo/enzona_api/blob/master/screenshot/enzona_api_aplicaciones1.png)

We enter our shop and in **Production Keys** we notice that we have two keys, **Consumer Key** and the **Consumer Secret**. Both keys must be copied in order to use the enzyme_api library.

![screenshot2](https://github.com/JosueCarballo/enzona_api/blob/master/screenshot/enzona_api_keys.png)

# Create a payment
    from enzona_api import enzona_business_payment
    
    ebp = enzona_business_payment(CONSUMER_KEY, CONSUMER_SECRET)
    
    SHIPPING = "10.00"
    TAX = "5.00"
    DISCOUNT = "2.00"
    TIP = "0.00"
    PRICE = "25.00"
    MERCHANT_OP_ID = "..." #your market identifier
    INVOICE_NUMBER = "..." #invoice number
    TERMINAL_ID = "..." #terminal identifier (POS, Cash Register, etc.)
    URL_RETURN = "www.example.com/return_payment"
    URL_CANCEL = "www.example.com/cancel_payment"
    
    pay = Payments(
        "My first pay",
        "Description pay",
        "Title pay",
        "CUP",
        SHIPPING,
        TAX,
        DISCOUNT,
        TIP,
        PRICE,
        MERCHANT_OP_ID,
        INVOICE_NUMBER,
        URL_RETURN,
        URL_CANCEL,
        TERMINAL_ID
    )
    
    response = ebp.create_payments(payment=pay.get_payment())
    href = response['links'][0]['href']
    
The value that acquires **href** is the return url of confirmation of the payment where it will have to direct to the user in order that this one realizes the payment from his account of Enzona. An interface is opened to view details, pay, authenticate if not logged into Enzona and select your payment cards.

![screenshot2](https://github.com/JosueCarballo/enzona_api/blob/master/screenshot/pago_enzona_web.png)

The url value set in **URL_RETURN** corresponds to the url that will redirect Enzona once the platform is successfully completed. **URL_CANCEL** is the url in case of cancellation. 

In case of an effective payment you must make a confirmation of the payment:

    ebp = enzona_business_payment(CONSUMER_KEY, CONSUMER_SECRET)
    response = ebp.complete_payments(transaction_uuid=request.GET["transaction_uuid"])

In case of cancellation of a payment:

    ebp = enzona_business_payment(CONSUMER_KEY, CONSUMER_SECRET)
    ebp.cancel_payments(transaction_uuid)

The value of **transaction_uuid** is returned with the URL_CANCEL set as a GET request (Example: www.example.com/cancel_payment?transaction_uuid=eff02133c1724287b10860824c596777).

**THIS DOCUMENTATION WILL CONTINUE**




