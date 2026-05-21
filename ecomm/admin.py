from django.contrib import admin
from .models import Custom_User, Category, Product, Order
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

# Register your models here.

# admin.site.register(Custom_User, UserAdmin)
@admin.register(Custom_User)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'phone', 'otp', 'is_verified']
    search_fields = ['username', 'email', 'phone',]
    list_filter = ['is_verified']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'created_at', 'image', 'slug']
    search_fields = ['name', 'slug']
    list_filter = ['name', 'created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ['view_image']
    list_display = ['name', 'id', 'price', 'is_available', 'view_image']
    search_fields = ['name', 'description', 'price']
    list_filter = ['category', 'is_available', 'created_at', 'updated_at']
    def view_image(self,obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} height="50%" width="50%">')
        else:
            return "Image not available"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('user', 'id', 'product', 'price', 'is_paid', 'status', 'connection_status', 'tran_time')
    search_fields=('user', 'product', 'category', 'price', )
    list_filter=('category', 'status', 'connection_status', 'tran_time',)