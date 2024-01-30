from django.contrib import admin
from .models import product
class ProductAdmin(admin.ModelAdmin):
    list__display=["id","pname","pcost","pdetails","cat","is_active"]

admin.site.register(product)
