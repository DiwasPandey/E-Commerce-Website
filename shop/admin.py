from django.contrib import admin
from .models import Product, Category, ProductHasImage

# Register your models here.

class ImageInline(admin.TabularInline):
    model = ProductHasImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)

