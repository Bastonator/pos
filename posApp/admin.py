from django.contrib import admin
from posApp.models import Category, Products, Sales, salesItems, Users, Branch

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Sales)
admin.site.register(salesItems)
admin.site.register(Users)
admin.site.register(Branch)
# admin.site.register(Employees)
