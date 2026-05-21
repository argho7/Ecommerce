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
    from .models import Order

    currency = "BDT"
    tran_id = uuid4()
    price = product.price
    user = request.user
    email =user.email
    phone = user.phone
    address = user.address
    city = user.city
    country = user.country
    
    product_name = product
    product_category = category

    post_body = {
    'total_amount' : price,
    'currency' : currency,
    'tran_id' : tran_id,
    'success_url' : request.build_absolute_uri('/payment/success/'),
    'fail_url' : request.build_absolute_uri('/payment/fail/'),
    'cancel_url' : request.build_absolute_uri('/payment/cancel/'),
    'emi_option' : 0,
    'cus_name' : user,
    'cus_email' : email,
    'cus_phone' : phone,
    'cus_add1' : address,
    'cus_city' : city,
    'cus_country' : country,
    'shipping_method' : "NO",
    'multi_card_name' : "",
    'num_of_item' : 1,
    'product_name' : product_name,
    'product_category' : product_category,
    'product_profile' : "test product profile",
    }

    response = sslcommez.createSession(post_body)

    con_status=response.get('status')
    tran_time=response.get('tran_time')
    session_key=response.get('sessionkey')

    Order.objects.create(connection_status=con_status, user=user, product=product_name, 
                         category=product_category, price=price, currency=currency, 
                         tran_id=tran_id, tran_time=tran_time, session_key=session_key)

    return response