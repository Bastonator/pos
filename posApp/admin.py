from django.contrib import admin
from posApp.models import Category, Products, Sales, salesItems, Users, Branch, Shifts, Lab_Shifts, Lab, Investigations, Test_performed,CustomerSales, CustomerSalesItems

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Sales)
admin.site.register(salesItems)
admin.site.register(Users)
admin.site.register(Branch)
admin.site.register(Shifts)
admin.site.register(Investigations)
admin.site.register(Test_performed)
admin.site.register(CustomerSales)
admin.site.register(CustomerSalesItems)

# admin.site.register(Employees)
