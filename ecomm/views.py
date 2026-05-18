from django.contrib import messages
from django.http import HttpResponse
from .models import Category, Product, Order, Custom_User
from .sslcommerz import initiate_sslcommerz_payment
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .utils import send_email, payment_system
from django.conf import settings
from django.core.mail import send_mail

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
    # print(product)
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
        "Test Subject",
        "This is a test email sent from Django via SMTP.",
        'sahaarghya2002@gmail.com'
    )
    
    # send_email(subject,message,from_email,receiver)
    context={}
    return render(request, 'search.html' )

    
def add_to_cart(request,product_id=None):
    context={}
    return render(request, 'search.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone = request.POST.get('phone') or None

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

        user = Custom_User.objects.create_user(username=username, email=email, password=password1)
        
        user.profile_picture = 'profile_pictures/default.png'
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')


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
    return render(request, 'payment_success.html')

@csrf_exempt
def payment_fail(request):
    return render(request, 'payment_fail.html')


def payment_cancel(request):
    return render(request, 'payment_cancel.html')

def payment_gate_auth_fail(request):
    return render(request, 'payment_gate_auth_fail.html')

