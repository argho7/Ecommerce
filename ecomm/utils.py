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



def payment_system(request, product, category):
    SSLCOMMERZ_settings = { 'store_id': settings.SSLCOMMERZ_STORE_ID, 
                'store_pass': settings.SSLCOMMERZ_STORE_PASSWORD,
                'issandbox': settings.SSLCOMMERZ_SANDBOX 
                }
    
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
    print(response['status'])
    print(response['sessionkey'])
    return response

def payment_info_sskey():
    settings = { 'store_id': 'testbox', 'store_pass': 'qwerty', 'issandbox': True }
    sslcommez = SSLCOMMERZ(settings)

    sessionkey = 'A8EF93B75B8107E4F36049E80B4F9149'
    response = sslcommez.transaction_query_session(sessionkey)
    print(response)