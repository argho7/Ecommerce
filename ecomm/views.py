import random
import string
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.contrib import messages
from .utils import send_email, payment_system
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, Custom_User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def home(request):
    categories = Category.objects.prefetch_related('product_set')
    context = {'categories': categories}
    return render(request, 'home.html', context)

def category_view(request, slug):
    categories=Category.objects.prefetch_related('product_set')
    specific_category=get_object_or_404(Category, slug=slug)
    products=Product.objects.filter(category=specific_category)
    context={'categories':categories,'specific_category':specific_category, 'products':products}
    return render(request, 'category.html', context)

def product_view(request, slug):
    product=get_object_or_404(Product, slug=slug)
    context={'product': product}
    return render(request, 'product_details.html', context)

def search(request):
    if request.method=='POST':
        search=request.POST.get('search')
        data=Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search))
        context={'products':data}
        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')
    
def cart(request):
    send_email(
        "Test Subject - "+str(datetime.now().strftime("%Y-%m-%d %I:%M %p")),
        "This is a test email sent from Django via SMTP.",
        settings.DEFAULT_FROM_EMAIL)
    context={}
    return render(request, 'search.html' )

def add_to_cart(request,product_id=None):
    return render(request, 'search.html',)

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address', '')
        user.city = request.POST.get('city', 'Khulna_default')
        user.country = request.POST.get('country', 'Bangladesh')
        
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'profile.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if Custom_User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        
        if Custom_User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')
        
        otp = generate_otp()
        
        user = Custom_User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            is_verified=False,
            otp=otp
        )
        
        send_email(
            'Verify Your Email - Eflyer',
            f'''Hello {username}, 
            
            Thank you for registering with Eflyer! 
            
            Your OTP for email verification is: {otp} 
            
            This OTP is valid for 10 minutes. 
            
            If you didn't request this, please ignore this email. 
            
            Best regards, 
            
            Eflyer Team ''',
            email,
        )
        
        messages.success(request, f'Verification OTP sent to {email}. Please verify your email.')
        return redirect('verify_email', user_id=user.id)
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not user.is_verified:
                messages.error(request, 'Please verify your email before logging in.')
                return redirect('verify_email', user_id=user.id)
            
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    category=Category.objects.get(product__id=product_id)
    
    response = payment_system(request,product,category)

    status=response["status"]
    if status == "SUCCESS":
        return redirect(response['GatewayPageURL'])
    else:
        return redirect('payment_gate_auth_fail')

@csrf_exempt
def payment_success(request):
    if request.method=='POST':
        response=request.POST

        amount=response.get('amount')
        tran_id=response.get('tran_id')
        tran_date=response.get('tran_date')

        product=Order.objects.get(tran_id = tran_id)
        product.status = response.get('status')
        product.is_paid = True
        product.val_id = response.get('val_id')
        product.card_type = response.get('card_type')
        product.store_amount = response.get('store_amount')
        product.bank_tran_id = response.get('bank_tran_id')
        product.card_issuer = response.get('card_issuer')
        product.card_brand = response.get('card_brand')
        product.card_sub_brand = response.get('card_sub_brand')
        product.card_issuer_country = response.get('card_issuer_country')
        product.card_issuer_country_code = response.get('card_issuer_country_code')
        product.store_id = response.get('store_id')
        product.verify_sign = response.get('verify_sign')
        product.verify_key = response.get('verify_key')
        product.verify_sign_sha2 = response.get('verify_sign_sha2')
        product.risk_level = response.get('risk_level')
        product.risk_title = response.get('risk_title')
        product.save()

        user_mail=product.user.email

        send_email(
            subject="Payment receipt",
            message=f"""Order complete : \n amount : {amount} \n transaction id : {tran_id} \n date : {tran_date}""",
            receiver=user_mail
        )
    return render(request, 'payment_success.html')

@csrf_exempt
def payment_fail(request):
    if request.method=='POST':
        response=request.POST
        print(response)
    return render(request, 'payment_fail.html')

def payment_cancel(request):
    return render(request, 'payment_cancel.html')

def payment_gate_auth_fail(request):
    return render(request, 'payment_gate_auth_fail.html')

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

def verify_email_view(request, user_id):
    user = Custom_User.objects.get(id=user_id)
    
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        
        if user.otp == entered_otp:
            user.is_verified = True
            user.otp = None
            user.save()
            messages.success(request, 'Email verified successfully! You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_email', user_id=user_id)
    
    return render(request, 'verify_email.html', {'user': user})

def resend_otp_view(request, user_id):
    user = Custom_User.objects.get(id=user_id)
    
    new_otp = generate_otp()
    user.otp = new_otp
    user.save()
    
    send_email(
        'New OTP for Email Verification - Eflyer',
        f'''Hello {user.username},
        
        Your new OTP is: {new_otp}
        
        This OTP is valid for 10 minutes.
        
        Best regards,
        Eflyer Team''',
        user.email,
        )
    
    messages.success(request, 'New OTP sent to your email.')
    return redirect('verify_email', user_id=user_id)