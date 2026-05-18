import requests
from django.conf import settings

def initiate_sslcommerz_payment(order):

    url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"

    payload = {
        'store_id': settings.SSLCOMMERZ_STORE_ID,
        'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
        'total_amount': order.price,
        'currency': 'BDT',
        'tran_id': order.id,

        'success_url': 'http://127.0.0.1:8000/payment/success/',
        'fail_url': 'http://127.0.0.1:8000/payment/fail/',
        'cancel_url': 'http://127.0.0.1:8000/payment/cancel/',

        'cus_name': order.user.username if order.user else "Guest",
        'cus_email': "test@gmail.com",
        'cus_phone': "01700000000",

        'shipping_method': "NO",
        'product_name': order.product.name,
        'product_category': "General",
        'product_profile': "general",
    }

    response = requests.post(url, data=payload)
    return response.json()