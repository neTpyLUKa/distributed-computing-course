from django.contrib import admin

from src.models import Product

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Product, ProductAdmin)