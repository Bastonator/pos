from datetime import datetime
from unicodedata import category
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import post_save


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, password, **other_fields)

    def create_user(self, email, username, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    country = CountryField()
    phone_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_absolute_url(self):
        return reverse("user-dash", kwargs={"pk": self.pk})

    def __str__(self):
        return self.email


class Branch(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True, auto_created=False)
    name = models.CharField(max_length=100, null=True)
    location = CountryField(null=True, blank=True)
    address = models.CharField(max_length=555, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    user = models.ManyToManyField(Users, related_name='branchusers', null=True)

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("home-page", kwargs={"pk": self.pk})


# class Employees(models.Model):
#     code = models.CharField(max_length=100,blank=True)
#     firstname = models.TextField()
#     middlename = models.TextField(blank=True,null= True)
#     lastname = models.TextField()
#     gender = models.TextField(blank=True,null= True)
#     dob = models.DateField(blank=True,null= True)
#     contact = models.TextField()
#     address = models.TextField()
#     email = models.TextField()
#     department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
#     position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
#     date_hired = models.DateField()
#     salary = models.FloatField(default=0)
#     status = models.IntegerField()
#     date_added = models.DateTimeField(default=timezone.now)
#     date_updated = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '
class Category(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='categorybranch', on_delete=models.CASCADE)
    #user = models.ForeignKey(Users, related_name="category", on_delete=models.DO_NOTHING, default=1, null=True, blank=True)

    def __str__(self):
        return self.name

class Products(models.Model):
    code = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    price = models.FloatField(default=0)
    cost_price = models.FloatField(default=0)
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='productsbranch', on_delete=models.CASCADE)
    stock = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    image = models.ImageField(null=True, blank=True)
    #user = models.ForeignKey(Users, related_name="products", on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return self.code + " - " + self.name

class Sales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='salesbranch', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='salesuser', on_delete=models.DO_NOTHING, null=True, default="wriberpos@gmail.com")

    def __str__(self):
        return self.code

    def sold_by(self):
        return self.user.email

    def branch(self):
        return self.branch_owner

    def code_again(self):
        return self.code

class salesItems(models.Model):
    sale_id = models.ForeignKey(Sales,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now, null=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='saleitembranch', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='saleitemuser', on_delete=models.DO_NOTHING, null=True)