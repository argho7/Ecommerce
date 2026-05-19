from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import Generate_Slug
# Create your models here.

class Custom_User(AbstractUser):
    phone=models.IntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.png', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10, blank=True, null=True)

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
    state_choices=[('Success','Successful'),
                   ('Fail', 'Failed'),
                   ('Cancel', 'Cancel'),
                   ('Unknown','Unknown')]
    
    user = models.ForeignKey(Custom_User, on_delete=models.DO_NOTHING, null = True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null = True)
    state=models.CharField(choices=state_choices, max_length=10, default='Unknown')
    tran_id=models.CharField(max_length=40, blank=True, null=True)
    val_id=models.CharField(max_length=40, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    card_type = models.CharField( max_length=50, blank=True, null=True)
    store_amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_no = models.CharField( max_length=50, blank=True, null=True)
    bank_tran_id = models.CharField( max_length=50, blank=True, null=True)
    status = models.CharField( max_length=50, blank=True, null=True)
    tran_time=models.DateTimeField(auto_now_add=True,  null=True)
    error = models.CharField( max_length=50, blank=True, null=True)
    currency = models.CharField( max_length=50,default="BDT", blank=True, null=True)
    stacard_issuertus = models.CharField( max_length=50, blank=True, null=True)
    card_brand = models.CharField( max_length=50, blank=True, null=True)
    card_sub_brand = models.CharField( max_length=50, blank=True, null=True)
    card_issuer_country = models.CharField( max_length=50, blank=True, null=True)
    card_issuer_country_code = models.CharField( max_length=50, blank=True, null=True)
    store_id = models.CharField( max_length=50, blank=True, null=True)
    verify_sign = models.CharField( max_length=50, blank=True, null=True)
    verify_key = models.TextField(blank=True, null=True)
    verify_sign_sha2 = models.CharField( max_length=100, blank=True, null=True)
    currency_type = models.CharField( max_length=50, blank=True, null=True)
    currency_amount = models.CharField( max_length=50, blank=True, null=True)
    currency_rate = models.CharField( max_length=50, blank=True, null=True)
    base_fair = models.CharField( max_length=50, blank=True, null=True)
    value_a = models.CharField( max_length=50, blank=True, null=True)
    value_b = models.CharField( max_length=50, blank=True, null=True)
    value_c = models.CharField( max_length=50, blank=True, null=True)
    value_d = models.CharField( max_length=50, blank=True, null=True)
    subscription_id = models.CharField( max_length=50, blank=True, null=True)
    risk_level = models.CharField( max_length=50, blank=True, null=True)
    risk_title = models.CharField( max_length=50, blank=True, null=True)
    