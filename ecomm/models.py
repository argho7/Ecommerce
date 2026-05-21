from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import Generate_Slug
# Create your models here.

class Custom_User(AbstractUser):
    phone=models.IntegerField(default="123456789", blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, blank=True, null=True)
    address=models.CharField(default="", max_length=50, blank=True, null=True)
    city=models.CharField(default="Khulna_default", max_length=20, blank=True, null=True)
    country=models.CharField(default="Bangladesh", max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug=Generate_Slug(Category, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING,)
    name = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self,  *args, **kwargs):
        if not self.slug:
            self.slug=Generate_Slug(Product, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING, null = True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False, null=True)
    status = models.CharField( max_length=50, blank=True, null=True)
    connection_status=models.CharField(max_length=10, default='Unknown', null=True, blank=True)
    tran_id=models.CharField(max_length=40, blank=True, null=True)
    session_key=models.CharField(max_length=40, blank=True, null=True)
    val_id=models.CharField(max_length=40, blank=True, null=True)
    card_type = models.CharField( max_length=50, blank=True, null=True)
    store_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    bank_tran_id = models.CharField( max_length=50, blank=True, null=True)
    tran_time=models.DateTimeField(auto_now_add=True,  null=True)
    error = models.CharField( max_length=50, default='', blank=True, null=True)
    currency = models.CharField(max_length=50,default="BDT", blank=True, null=True)
    card_issuer = models.CharField( max_length=50, blank=True, null=True)
    card_brand = models.CharField( max_length=50, blank=True, null=True)
    card_sub_brand = models.CharField( max_length=50, blank=True, null=True)
    card_issuer_country = models.CharField( max_length=50, blank=True, null=True)
    card_issuer_country_code = models.CharField( max_length=50, blank=True, null=True)
    store_id = models.CharField( max_length=50, blank=True, null=True)
    verify_sign = models.CharField( max_length=50, blank=True, null=True)
    verify_key = models.TextField(blank=True, null=True)
    verify_sign_sha2 = models.CharField( max_length=100, blank=True, null=True)
    risk_level = models.CharField( max_length=5, blank=True, null=True)
    risk_title = models.CharField( max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user}+{self.product}"