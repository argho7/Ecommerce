from uuid import uuid4
from django.utils.text import slugify
from django.core.mail import send_mail
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ 

def Generate_Slug(model, name):
    slug=slugify(name)

    while model.objects.filter(slug=slug).exists():
        slug=slug + str(uuid4())[:4]
    return slug

def send_email(subject=None, message=None, receiver=None ):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [receiver],
        False,
    )


SSLCOMMERZ_settings = { 'store_id': settings.SSLCOMMERZ_STORE_ID, 
            'store_pass': settings.SSLCOMMERZ_STORE_PASSWORD,
            'issandbox': settings.SSLCOMMERZ_SANDBOX 
            }

def payment_system(request, product, category):
    sslcommez = SSLCOMMERZ(SSLCOMMERZ_settings)
    post_body = {
    'total_amount' : product.price,
    'currency' : "BDT",
    'tran_id' : uuid4(),
    'success_url' : request.build_absolute_uri('/payment/success/'),
    'fail_url' : request.build_absolute_uri('/payment/fail/'),
    'cancel_url' : request.build_absolute_uri('/payment/cancel/'),
    'emi_option' : 0,
    'cus_name' : request.user,
    'cus_email' : request.user.email,
    'cus_phone' : "01783555555",
    'cus_add1' : "customer address",
    'cus_city' : "Dhaka",
    'cus_country' : "Bangladesh",
    'shipping_method' : "NO",
    'multi_card_name' : "",
    'num_of_item' : 1,
    'product_name' : product.name,
    'product_category' : category,
    'product_profile' : "general",
    }

    response = sslcommez.createSession(post_body)
    # print(response)
    return response