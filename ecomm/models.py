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
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
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
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    state=models.CharField(choices=state_choices, max_length=10, default='Unknown')
    time=models.DateTimeField(auto_now_add=True,  null=True)

    