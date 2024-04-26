from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse
from flask import jsonify
from posApp.models import Category, Products, CustomerSales, Customer, Supplier, CustomerSalesItems, Sales, salesItems, Shifts, ProductChange, changeItems, Move, Lab, LipidProfile_Test, Liver_Function_Test, Renal_Function_Test, Ironprofile_Test, Inflammtory_Test
from posApp.models import Ascetic_Fluid_Test, Elements_conc_Test, Pancreatic_enzymes_Test, Test_performed, Patient, Reproduction, Investigations, Diabetic_Test, Autoimmunity_and_cancer_Test, Cardiac_Markers, Complaint, Prescription
from django.db.models import Count, Sum
from posApp.models import Branch, Users
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from pos.settings import LOW_INVENTORY
from django.db.models.functions import Now
import json, sys
from datetime import date, datetime
from posApp.forms import RegistrationForm, BranchForm, CustomerForm, SupplierForm, CategoryForm, ProductForm, SaleForm, MoveForm, LipidForm, LiverForm, ElectrolytesForm, AsceticForm, AandCForm, ReproductionForm, RenalForm, DiabeticForm, CardiacForm, IronForm, InflammatoryForm, InvestigationForm, PancreaticForm, ComplaintForm, PrescriptionForm
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template


# Login
def login_user(request):
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


def login_account(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(user.get_absolute_url())
            # Redirect to a success page.
        else:
            messages.success(request, ('Error, invalid password or username, try Again'))
            return redirect('login-me')
            # Return an 'invalid login' error message.
    return render(request, 'login-form-v8/Login_v8/loginv8.html', {})


# Logout
def logoutuser(request):
    logout(request)
    return redirect('login-me')


# Create your views here.
def index(request):
    return render(request, 'posApp/landingpage.html')


def user_account(request, pk):
    user = Users.objects.get(email=pk)
    branch = Branch.objects.filter(user=pk)

    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")

    Final_total = int()

    sold = int()

    for sale in branch:
        total_sales = Sales.objects.filter(
            date_added__year=current_year,
            date_added__month=current_month,
            date_added__day=current_day
        ).filter(branch_owner_id=sale.id)
        print(total_sales)

        selling = len(total_sales)

        sold = sold + selling

        for total in total_sales:
            Total = 0
            Total = Total + total.grand_total
            print(Total)

            Final_total = Final_total + Total

    branch_num = len(branch)

    return render(request, 'posApp/index.html',
                  {'user': user, 'branch': branch, 'Total_for_day': Final_total, 'sold': sold, 'branch_num': branch_num})


def branches(request, pk):
    user = Users.objects.get(email=pk)
    branch = Branch.objects.filter(user=pk)
    return render(request, 'posApp/tables-data.html', {'user': user, 'branch': branch})


def account_register(request):
    if request.method == 'POST':
        registerform = RegistrationForm(request.POST)
        if registerform.is_valid():
            user = registerform.save(commit=False)
            user.email = registerform.cleaned_data['email']
            user.set_password(registerform.cleaned_data['password1'])
            user.is_active = True
            user.save()
            return redirect(user.get_absolute_url())
    else:
        registerform = RegistrationForm()
    return render(request, 'posApp/user_register.html', {'form': registerform})


@login_required
def branch_register(request, pk):
    users = Users.objects.get(email=pk)
    # user = Branch.objects.filter(user=request.user)
    userrrs = Users.objects.all()
    context = {'userrrs': userrrs, 'users': users}
    if request.method == "POST":
        # form = BranchForm(request.POST or None)
        # branch = form
        branch_id = request.POST.get('branchid')
        branch_name = request.POST.get('branchname')
        # branch.location = request.POST['branchlocation']
        branch_address = request.POST.get('branchaddress')
        branch_phone = request.POST.get('phone')
        branch_user = request.POST.get('user1')
        branch = Branch.objects.create(id=branch_id, name=branch_name, location=None, address=branch_address, phone=branch_phone)
        branch.user.add(branch_user or None)
        # it is branch.user.add because user is how the many to many field is designated in the models.py
        context['branchid'] = branch
        context['created'] = True
    return render(request, 'posApp/tables-general.html', context=context)


@login_required
def branch_users(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    users = branch.user.all()
    user = Users.objects.get(email=pk1)
    return render(request, 'posApp/branch_users.html', {'branch': branch, 'users': users, 'user': user})


@login_required
def delete_branch_users(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    #user = Users.objects.get(email=pk)
    branch.user.remove(Users.objects.get(email=pk1))
    return render(request, 'posApp/home.html', {'branch': branch})


@login_required
def manage_users(request, pk):
    branch = Branch.objects.get(id=pk)
    users = Users.objects.all()
    context = {
        'branch': branch,
        'users': users,
    }
    if request.method == "POST":
        new_user = request.POST.get('new_user')
        branch_user = Branch.objects.get(id=pk)
        branch_user.user.add(new_user or None)
        return render(request, 'posApp/new_user_alert.html', context)
    return render(request, 'posApp/manage_users.html', context)


@login_required
def home(request, pk):
    if request.user.is_authenticated:
        branch = Branch.objects.get(id=pk)
        users = branch.user.all()
        now = datetime.now()
        current_year = now.strftime("%Y")
        current_month = now.strftime("%m")
        current_day = now.strftime("%d")
        categories = len(Category.objects.filter(branch_owner_id=pk))
        products = len(Products.objects.filter(branch_owner_id=pk))
        transaction = len(Sales.objects.filter(
            date_added__year=current_year,
            date_added__month=current_month,
            date_added__day=current_day
        ).filter(branch_owner_id=pk))
        today_sales = Sales.objects.filter(
            date_added__year=current_year,
            date_added__month=current_month,
            date_added__day=current_day
        ).filter(branch_owner_id=pk)
        total_sales = sum(today_sales.values_list('grand_total', flat=True))
        context = {
            'page_title': 'Home',
            'categories': categories,
            'products': products,
            'transaction': transaction,
            'total_sales': total_sales,
            'branch': branch
        }
        return render(request, 'posApp/home.html', context)
    else:
        return redirect('login-me')


def about(request):
    context = {
        'page_title': 'About',
    }
    return render(request, 'posApp/about.html', context)


@login_required
def all_customer(request, pk):
    user = Users.objects.get(email=pk)
    customer = Customer.objects.filter(created_by_id=pk)
    context = {
        'user': user,
        'customer': customer
    }
    return render(request, 'posApp/customers.html', context=context)


@login_required
def new_customer(request, pk):
    user = Users.objects.get(email=pk)
    form = CustomerForm(request.POST or None, request.FILES or None)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()

            customer.branch_owner.set(form.cleaned_data['branch_owner'] or None)
            return render(request, 'posApp/newcustomeralert.html', {'user': user, 'form': form})
    else:
        form.fields["branch_owner"].queryset = Branch.objects.filter(user=request.user)
    return render(request, 'posApp/newcustomer.html', context=context)


@login_required
def choose_customer(request, pk):
    branch = Branch.objects.get(id=pk)
    customers = Customer.objects.filter(branch_owner=pk).order_by('-id')
    context = {'branch': branch, 'customers': customers}
    return render(request, 'posApp/branch_customers.html', context)


@login_required
def customer_pos(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    customers = Customer.objects.get(id=pk1)
    products = Products.objects.filter(branch_owner_id=pk, status=1)
    product_json = []
    for product in products:
        product_json.append({'id': product.id, 'name': product.name, 'price': float(product.price)})
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'product_json': json.dumps(product_json),
        'branch': branch,
        'branch1': branch1,
        'customers': customers
    }
    # return HttpResponse('')
    return render(request, 'posApp/customerpos.html', context)


@login_required
def customer_checkout_modal(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    customers = Customer.objects.get(id=pk1)
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total': grand_total,
        'branch': branch,
        'customers': customers
    }
    return render(request, 'posApp/customercheckout.html', context)


@login_required
def save_customer_pos(request, pk, pk1):
    resp = {'status': 'failed', 'msg': ''}
    branch = Branch.objects.get(id=pk)
    customers = Customer.objects.get(id=pk1)
    shift = Shifts.objects.filter(branch_owner_id=pk).last()
    data = request.POST
    seller = Users.objects.get(email=request.user)
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = CustomerSales.objects.filter(code=str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        sales = CustomerSales(code=code, sub_total=data['sub_total'], tax=data['tax'], tax_amount=data['tax_amount'],
                      grand_total=data['grand_total'], tendered_amount=data['tendered_amount'],
                      amount_change=data['amount_change'], branch_owner=branch, user=seller, shift_sold=shift, customer=customers,
                              is_paid= True if request.POST.getlist('invoice', False) else False, due_date=request.POST.get('due-date'), terms_conditions=request.POST.get('terms')).save()
        print(request.POST.getlist('invoice'))
        sale_id = CustomerSales.objects.last().pk
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod
            sale = CustomerSales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i]
            price = data.getlist('price[]')[i]
            total = float(qty) * float(price)
            product.stock = product.stock - float(qty)
            product.save()
            print(customers)
            print({'sale_id': sale, 'product_id': product, 'qty': qty, 'price': price, 'total': total, 'shift_sold': shift, 'customer': customers})
            CustomerSalesItems(sale_id=sale, product_id=product, qty=qty, price=price, total=total, branch_owner=branch,
                       user=seller, shift_sold=shift, customer=customers).save()
            i += int(1)
        resp['status'] = 'success'
        resp['sale_id']  = sale_id
        messages.success(request, "Sale Record has been saved.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
        raise ValueError()
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def customer_receipt(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    customers = Customer.objects.get(id=pk1)
    id = request.GET.get('id')
    sales = CustomerSales.objects.filter(branch_owner_id=pk, id=id).first()
    transaction = {}
    for field in CustomerSales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales, field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = CustomerSalesItems.objects.filter(sale_id=sales).all()
    context = {
        "transaction": transaction,
        "salesItems": ItemList,
        'branch': branch,
        'customers': customers
    }

    return render(request, 'posApp/receipt.html', context)


@login_required
def Customer_salesList(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    customers = Customer.objects.get(id=pk1)
    sales = CustomerSales.objects.filter(customer=pk1).order_by('-id')
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        data['items'] = CustomerSalesItems.objects.filter(sale_id=sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']), '.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)

    p = Paginator(sales, 25)

    page_num = request.GET.get('page_sale', 1)
    try:
        page_sale = p.page(page_num)
    except EmptyPage:
        page_sale = p.page(1)

    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
        'branch': branch,
        'branch1': branch1,
        'sales': sales,
        'list': page_sale,
        'customers': customers
    }
    # return HttpResponse('')
    return render(request, 'posApp/customersales.html', context)


@login_required
def manage_customer_sales(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    customers = Customer.objects.get(id=pk1)

    sales = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            sales = CustomerSales.objects.filter(branch_owner_id=pk, id=id).first()

    context = {
        'sales': sales,
        'branch': branch,
        'customers': customers
    }
    return render(request, 'posApp/manage_sales.html', context)

@login_required
def save_sale_changes(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    customers = Customer.objects.get(id=pk1)
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_customersale = CustomerSales.objects.filter(id=data['id']).update(is_paid=True if request.POST.getlist('invoice', False) else False)
        resp['status'] = 'success'
        messages.success(request, 'Paid status change Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_customer_sale(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    customers = Customer.objects.get(id=pk1)
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        delete = CustomerSales.objects.filter(id=id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def all_suppliers(request, pk):
    user = Users.objects.get(email=pk)
    suppliers = Supplier.objects.filter(created_by_id=pk)
    context = {
        'user': user,
        'suppliers': suppliers
    }
    return render(request, 'posApp/suppliers.html', context=context)


@login_required
def new_suppliers(request, pk):
    user = Users.objects.get(email=pk)
    form = SupplierForm(request.POST or None, request.FILES or None)
    context = {'user': user, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()

            customer.branch_owner.set(form.cleaned_data['branch_owner'] or None)
            return render(request, 'posApp/newsupplieralert.html', {'user': user, 'form': form})
    else:
        form.fields["branch_owner"].queryset = Branch.objects.filter(user=request.user)
    return render(request, 'posApp/newsupplier.html', context=context)


@login_required
def view_invoice(request, pk, pk1, pk2):
    branch = Branch.objects.get(id=pk)
    customers = Customer.objects.get(id=pk1)
    customer_sales = CustomerSales.objects.get(id=pk2)
    customer_sales_items = CustomerSalesItems.objects.filter(sale_id=pk2)
    grand_total = customer_sales.grand_total + customer_sales.tax_amount
    context = {
        'branch': branch,
        'customers': customers,
        'customer_sales': customer_sales,
        'customer_sales_items': customer_sales_items,
        'grand_total': grand_total
    }
    return render(request, 'docs/index.html', context)


# Categories
@login_required
def addnew_cat(request, pk):
    branch1 = Branch.objects.get(id=pk)
    branch2 = Branch.objects.get(id=pk)
    branch = Branch.objects.filter(user=request.user)
    form = CategoryForm(request.POST or None, request.FILES or None)
    context = {'branch': branch, 'branch1': branch1, 'branch2': branch2, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            cat = form.save(commit=False)
            # cat.user = request.user
            cat.save()
            return redirect('home')
    else:
        form.fields["branch_owner"].queryset = Branch.objects.filter(user=request.user)
    return render(request, 'posApp/catadd.html', context=context)


@login_required
def category(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    category_list = Category.objects.filter(branch_owner_id=pk)
    # category_list = {}
    context = {
        'page_title': 'Category List',
        'category': category_list,
        'branch': branch,
        'branch1': branch1,
    }
    return render(request, 'posApp/category.html', context)


@login_required
def manage_category(request, pk):
    branch = Branch.objects.get(id=pk)
    category = {}
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(branch_owner_id=pk, id=id).first()

    context = {
        'category': category,
        'branch': branch
    }
    return render(request, 'posApp/manage_category.html', context)


@login_required
def save_category(request, pk):
    branch = Branch.objects.get(id=pk)
    data = request.POST
    resp = {'status': 'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0:
            save_category = Category.objects.filter(id=data['id']).update(name=data['name'],
                                                                          description=data['description'],
                                                                          status=data['status'])
        else:
            save_category = Category(name=data['name'], description=data['description'], status=data['status'],
                                     branch_owner=branch)
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_category(request, pk):
    branch = Branch.objects.get(id=pk)
    data = request.POST
    resp = {'status': ''}
    try:
        Category.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


# Products
@login_required
def addnew_prod(request, pk):
    branch1 = Branch.objects.get(id=pk)
    branch2 = Branch.objects.get(id=pk)
    branch = Branch.objects.filter(user=request.user)
    categories = Category.objects.filter(branch_owner_id=pk, status=1).all()
    form = ProductForm(request.POST or None, request.FILES or None)
    context = {'branch': branch, 'branch1': branch1, 'branch2': branch2, 'categories': categories, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            prod = form.save(commit=False)
            # cat.user = request.user
            prod.save()
            return redirect('home')
    else:
        form.fields["branch_owner"].queryset = Branch.objects.filter(user=request.user)
    return render(request, 'posApp/prodadd.html', context=context)


@login_required
def search_products(request, pk):
    branch = Branch.objects.get(id=pk)

    if request.method == "POST":
        search_str = request.POST['search_str']
        products = Products.objects.filter(
            name__icontains=search_str, branch_owner=branch) | Products.objects.filter(
            description__icontains=search_str, branch_owner=branch) | Products.objects.filter(
            price__icontains=search_str, branch_owner=branch) | Products.objects.filter(
            supplier__icontains=search_str, branch_owner=branch) | Products.objects.filter(
            expiry_date__icontains=search_str, branch_owner=branch) | Products.objects.filter(category_id__name__icontains=search_str, branch_owner=branch)

        p = Paginator(products, 40)

        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)

        low_inventory = Products.objects.filter(
            branch_owner_id=pk, stock__lte=LOW_INVENTORY
        )

        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item has low inventory')

        low_inventory_ids = Products.objects.filter(
            branch_owner_id=pk, stock__lte=LOW_INVENTORY
        ).values_list('id', flat=True)

        expired_products = Products.objects.filter(
            branch_owner_id=pk, expiry_date__lte=Now()
        ) | Products.objects.filter(
            branch_owner_id=pk, expiry_date=None)

        if expired_products.count() > 0:
            if expired_products.count() > 1:
                messages.error(request, f'{expired_products.count()} items are expired or about to be expired')
            else:
                messages.error(request, f'{expired_products.count()} item is expired or about to be expired')

        expired_products_ids = Products.objects.filter(
            branch_owner_id=pk, expiry_date__lte=Now()
        ).values_list('expiry_date', flat=True)

        return render(request, 'posApp/productsearch.html',
                      {'branch': branch, 'search_str': search_str, 'products': products, 'product_list': page,
                       'low_inventory_ids': low_inventory_ids, 'expired_products_ids': expired_products_ids})
    else:
        return render(request, 'posApp/productsearch.html', {'branch': branch})



@login_required
def products(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    product_list = Products.objects.filter(branch_owner_id=pk).order_by('name')

    p = Paginator(product_list, 35)

    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    low_inventory = Products.objects.filter(
        branch_owner_id=pk, stock__lte=LOW_INVENTORY
    )

    if low_inventory.count() > 0:
        if low_inventory.count() > 1:
            messages.error(request, f'{low_inventory.count()} items have low inventory')
        else:
            messages.error(request, f'{low_inventory.count()} item has low inventory')

    low_inventory_ids = Products.objects.filter(
        branch_owner_id=pk, stock__lte=LOW_INVENTORY
    ).values_list('id', flat=True)

    expired_products = Products.objects.filter(
        branch_owner_id=pk, expiry_date__lte=Now()
    ) | Products.objects.filter(
        branch_owner_id=pk, expiry_date=None)

    if expired_products.count() > 0:
        if expired_products.count() > 1:
            messages.error(request, f'{expired_products.count()} items are expired or about to be expired')
        else:
            messages.error(request, f'{expired_products.count()} item is expired or about to be expired')

    expired_products_ids = Products.objects.filter(
        branch_owner_id=pk, expiry_date__lte=Now()
    ).values_list('expiry_date', flat=True)

    context = {
        'page_title': 'Product List',
        'products': page,
        'product_list': product_list,
        'branch': branch,
        'branch1': branch1,
        'low_inventory_ids': low_inventory_ids,
        'expired_products_ids': expired_products_ids
    }
    return render(request, 'posApp/products.html', context)


@login_required
def low_products(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    product_list = Products.objects.filter(branch_owner_id=pk).order_by('stock')

    p = Paginator(product_list, 35)

    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    low_inventory = Products.objects.filter(
        branch_owner_id=pk, stock__lte=LOW_INVENTORY
    )

    if low_inventory.count() > 0:
        if low_inventory.count() > 1:
            messages.error(request, f'{low_inventory.count()} items have low inventory')
        else:
            messages.error(request, f'{low_inventory.count()} item has low inventory')

    low_inventory_ids = Products.objects.filter(
        branch_owner_id=pk, stock__lte=LOW_INVENTORY
    ).values_list('id', flat=True)

    expired_products = Products.objects.filter(
        branch_owner_id=pk, expiry_date__lte=Now()
    ) | Products.objects.filter(
        branch_owner_id=pk, expiry_date=None)

    if expired_products.count() > 0:
        if expired_products.count() > 1:
            messages.error(request, f'{expired_products.count()} items are expired or about to be expired')
        else:
            messages.error(request, f'{expired_products.count()} item is expired or about to be expired')

    expired_products_ids = Products.objects.filter(
        branch_owner_id=pk, expiry_date__lte=Now()
    ).values_list('expiry_date', flat=True)

    context = {
        'page_title': 'Product List',
        'products': page,
        'product_list': product_list,
        'branch': branch,
        'branch1': branch1,
        'low_inventory_ids': low_inventory_ids,
        'expired_products_ids': expired_products_ids
    }
    return render(request, 'posApp/low_products.html', context)

@login_required
def manage_products(request, pk):
    branch = Branch.objects.get(id=pk)
    suppliers = Supplier.objects.filter(branch_owner=pk)
    product = {}
    categories = Category.objects.filter(branch_owner_id=pk, status=1).all()
    if request.method == 'GET':
        data = request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(branch_owner_id=pk, id=id).first()

    context = {
        'product': product,
        'categories': categories,
        'branch': branch,
        'suppliers': suppliers
    }
    return render(request, 'posApp/manage_product.html', context)


def test(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'posApp/test.html', context)


@login_required
def save_product(request, pk):
    branch = Branch.objects.get(id=pk)
    data = request.POST
    resp = {'status': 'failed'}
    id = ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0:
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id=data['category_id']).first()
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0:
                save_product = Products.objects.filter(id=data['id']).update(code=data['code'], category_id=category,
                                                                             name=data['name'],
                                                                             description=data['description'],
                                                                             price=float(data['price']),
                                                                             cost_price=float(data['cost_price']),
                                                                             status=data['status'],
                                                                             stock=int(data['stock']),
                                                                             expiry_date=request.POST.get('date'),
                                                                             image=request.FILES['img'], suppliers=data['suppliers'])
            else:
                save_product = Products(code=data['code'], category_id=category, name=data['name'],
                                        description=data['description'], price=float(data['price']),
                                        cost_price=float(data['cost_price']),
                                        status=data['status'], stock=int(data['stock']), branch_owner=branch,
                                        expiry_date=request.POST.get('date'), image=request.FILES['img'])
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_product(request, pk):
    branch = Branch.objects.get(id=pk)
    data = request.POST
    resp = {'status': ''}
    try:
        Products.objects.filter(id=data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def shift_list(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    shifts = Shifts.objects.filter(branch_owner_id=pk).order_by('-id')
    return render(request, 'posApp/shifts.html', {'branch': branch, 'branch1': branch1, 'shifts': shifts})


def start_shift(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    context = {'branch': branch, 'branch1': branch1}
    if request.method == "POST":
        name = request.POST.get('shift_name')
        shift = Shifts.objects.create(name=name, branch_owner=branch, user=request.user)
        context['shiftid'] = shift
        context['created'] = True
    return render(request, 'posApp/startshift.html', context=context)


def shift_sales(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    shift = Shifts.objects.get(id=pk1)
    sales = Sales.objects.filter(shift_sold_id=pk1)
    total = 0

    for sale in sales:
        total = total + sale.grand_total
        print(total)

    shift.shift_sales = total
    return render(request, 'posApp/shiftsales.html', {'branch': branch, 'branch1': branch1, 'shift': shift, 'sales': sales, 'total': total})


def shift_sale_items(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    shift = Shifts.objects.get(id=pk1)
    sales = Sales.objects.filter(shift_sold_id=pk1).order_by('-id')
    #did't work till i added sale data and made the data render in a list format. ofcourse i appeded the data at the end.
    sale_data = []

    for sale in sales:
        item = sale
        for prod in salesItems.objects.filter(sale_id=item).order_by('-id'):
            print(prod)
            stuff = prod
            sale_data.append(stuff)

        total = 0

        for sale in sales:
            total = total + sale.grand_total
            print(total)

        shift.shift_sales = total

        #data = salesItems.objects.filter(sale_id=item)

    context = {
        'branch': branch,
        'branch1': branch1,
        'shift': shift,
        'sales': sales,
        'sale_data': sale_data
    }
    return render(request, 'posApp/shiftsaleitems.html', context)

@login_required
def pos(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    products = Products.objects.filter(branch_owner_id=pk, status=1, stock__gt=0)
    product_json = []
    for product in products:
        product_json.append({'id': product.id, 'name': product.name, 'price': float(product.price)})
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'product_json': json.dumps(product_json),
        'branch': branch,
        'branch1': branch1,
    }
    # return HttpResponse('')
    return render(request, 'posApp/pos.html', context)


@login_required
def checkout_modal(request, pk):
    branch = Branch.objects.get(id=pk)
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total': grand_total,
        'branch': branch
    }
    return render(request, 'posApp/checkout.html', context)


@login_required
def save_pos(request, pk):
    resp = {'status': 'failed', 'msg': ''}
    branch = Branch.objects.get(id=pk)
    shift = Shifts.objects.filter(branch_owner_id=pk).last()
    data = request.POST
    seller = Users.objects.get(email=request.user)
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code=str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        sales = Sales(code=code, sub_total=data['sub_total'], tax=data['tax'], tax_amount=data['tax_amount'],
                      grand_total=data['grand_total'], tendered_amount=data['tendered_amount'],
                      amount_change=data['amount_change'], branch_owner=branch, user=seller, shift_sold=shift).save()
        sale_id = Sales.objects.last().pk
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod
            sale = Sales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i]
            price = data.getlist('price[]')[i]
            total = float(qty) * float(price)
            product.stock = product.stock - float(qty)
            product.save()
            print({'sale_id': sale, 'product_id': product, 'qty': qty, 'price': price, 'total': total})
            salesItems(sale_id=sale, product_id=product, qty=qty, price=price, total=total, branch_owner=branch, user=seller).save()
            i += int(1)
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Sale Record has been saved.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def addnew_sale(request, pk):
    branch1 = Branch.objects.get(id=pk)
    branch2 = Branch.objects.get(id=pk)
    branch = Branch.objects.filter(user=request.user)
    form = SaleForm(request.POST or None, request.FILES or None)
    context = {'branch': branch, 'branch1': branch1, 'branch2': branch2, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            sale = form.save(commit=False)
            # cat.user = request.user
            sale.save()
            return redirect('home')
    else:
        form.fields["branch_owner"].queryset = Branch.objects.filter(user=request.user)
    return render(request, 'posApp/saleadd.html', context=context)


@login_required
def salesList(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    sales = Sales.objects.filter(branch_owner_id=pk).order_by('-id')
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        data['items'] = salesItems.objects.filter(sale_id=sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']), '.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)

    p = Paginator(sales, 35)

    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
        'branch': branch,
        'branch1': branch1,
        'sales': sales,
        'list': page,
    }
    # return HttpResponse('')
    return render(request, 'posApp/sales.html', context)


@login_required
def receipt(request, pk):
    branch = Branch.objects.get(id=pk)
    id = request.GET.get('id')
    sales = Sales.objects.filter(branch_owner_id=pk, id=id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales, field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id=sales).all()
    context = {
        "transaction": transaction,
        "salesItems": ItemList,
        'branch': branch
    }

    return render(request, 'posApp/newreceipt.html', context)
    # return HttpResponse('')


@login_required
def delete_sale(request, pk):
    branch = Branch.objects.get(id=pk)
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id=id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def inventory(request, pk):
    branch = Branch.objects.get(id=pk)
    products = Products.objects.filter(branch_owner_id=pk).order_by('name')
    return render(request, 'posApp/inventory.html', {'branch': branch, 'products': products})


@login_required
def todays_sales(request, pk):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    branch = Branch.objects.get(id=pk)
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month=current_month,
        date_added__day=current_day
    ).filter(branch_owner_id=pk).order_by('-id')
    return render(request, 'posApp/todays_sales.html', {'branch': branch, 'today_sales': today_sales})


@login_required
def todays_sale_items(request, pk):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    branch = Branch.objects.get(id=pk)
    todays_sale_items = salesItems.objects.filter(
        date_added__year=current_year,
        date_added__month=current_month,
        date_added__day=current_day
    ).filter(branch_owner_id=pk).order_by('-id')
    return render(request, 'posApp/todays_sale_items.html', {'branch': branch, 'todays_sale_items': todays_sale_items})


@login_required
def product_change(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    suppliers = Supplier.objects.filter(branch_owner=pk)
    products = Products.objects.filter(branch_owner_id=pk, status=1)
    product_json = []
    for product in products:
        product_json.append({'id': product.id, 'name': product.name, 'cost_price': float(product.cost_price), 'stock' : int(product.stock)})
    context = {
        'page_title': "Point of Sale",
        'products': products,
        'product_json': json.dumps(product_json),
        'branch': branch,
        'branch1': branch1,
        'suppliers': suppliers
    }
    # return HttpResponse('')
    return render(request, 'posApp/productchange.html', context)



@login_required
def change_modal(request, pk):
    branch = Branch.objects.get(id=pk)
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {
        'grand_total': grand_total,
        'branch': branch
    }
    return render(request, 'posApp/stockchange_checkout.html', context)


@login_required
def save_change(request, pk):
    resp = {'status': 'failed', 'msg': ''}
    branch = Branch.objects.get(id=pk)
    data = request.POST
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = ProductChange.objects.filter(code=str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        suppliers = request.POST.get('supply-from')
        supplier_forchange = Supplier.objects.get(id=suppliers)

        change = ProductChange(code=code, sub_total=data['sub_total'], tax=data['tax'], tax_amount=data['tax_amount'],
                               grand_total=data['grand_total'], tendered_amount=data['tendered_amount'],
                               amount_change=data['amount_change'], branch_owner=branch, user=request.user, suppliers=supplier_forchange).save()
        change_id = ProductChange.objects.last().pk
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod
            change = ProductChange.objects.filter(id=change_id).first()
            product = Products.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i]
            price = data.getlist('cost_price[]')[i]
            supplier = data['suppliers']
            print(supplier)
            supplier_id = Supplier.objects.get(id=supplier)
            new_costprice = data.getlist('cost_price[]')[i]
            total = float(qty) * float(price)
            product.stock = product.stock + float(qty)
            product.suppliers = supplier_id
            product.cost_price = new_costprice
            product.save()
            print({'change_id': change, 'product_id': product, 'qty': qty, 'price': price, 'total': total})
            changeItems(change_id=change, product_id=product, qty=qty, price=new_costprice, total=total,
                        branch_owner=branch).save()
            i += int(1)
        resp['status'] = 'success'
        resp['change_id'] = change_id
        messages.success(request, "Stock has been added.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
        raise ValueError()
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def receipt_forstock(request, pk):
    branch = Branch.objects.get(id=pk)
    id = request.GET.get('id')
    change = ProductChange.objects.filter(branch_owner_id=pk, id=id).first()
    transaction = {}
    for field in ProductChange._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(ProductChange, field.name)
    ItemList = changeItems.objects.filter(change_id=change).all()

    total = 0
    for sale in ItemList:
        total = total + sale.total
        print(total)

    context = {
        "transaction": transaction,
        "salesItems": ItemList,
        'branch': branch,
        'total': total
    }

    return render(request, 'posApp/stockchange_receipt.html', context)


@login_required
def view_newstocklist(request, pk):
    branch = Branch.objects.get(id=pk)
    stock = ProductChange.objects.filter(branch_owner=pk).order_by('-id')
    sale_data = []
    for sale in stock:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        data['items'] = changeItems.objects.filter(change_id=sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']), '.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)

    p = Paginator(stock, 20)

    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
        'branch': branch,
        'sales': stock,
        'list': page
    }
    # return HttpResponse('')
    return render(request, 'posApp/branch_newstock.html', context)

@login_required
def delete_newstock(request, pk):
    branch = Branch.objects.get(id=pk)
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        delete = ProductChange.objects.filter(id=id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Stock Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def view_supplierlist(request, pk):
    branch = Branch.objects.get(id=pk)
    supplier = Supplier.objects.filter(branch_owner=pk)
    context = {
        'branch': branch,
        'supplier': supplier
    }
    return render(request, 'posApp/branch_suppliers.html', context)


@login_required
def view_suppliernewstock(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    supplier = Supplier.objects.get(id=pk1)
    stock = ProductChange.objects.filter(branch_owner=pk, suppliers=pk1).order_by('-id')
    sale_data = []
    for sale in stock:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale, field.name)
        data['items'] = changeItems.objects.filter(change_id=sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']), '.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)

    p = Paginator(stock, 20)

    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except EmptyPage:
        page = p.page(1)

    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
        'branch': branch,
        'sales': stock,
        'list': page,
        'supplier': supplier
    }
    return render(request, 'posApp/branch_supplierstock.html', context)


@login_required
def delete_newsupplierstock(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    supplier = Supplier.objects.get(id=pk1)
    resp = {'status': 'failed', 'msg': ''}
    id = request.POST.get('id')
    try:
        delete = ProductChange.objects.filter(id=id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Stock Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def dashboard_suppliernewstock(request, pk, pk1):
    user = Users.objects.get(email=pk)
    supplier = Supplier.objects.get(id=pk1)
    stock = ProductChange.objects.filter(suppliers=pk1).order_by('-id')
    context = {
        'user': user,
        'supplier': supplier,
        'stock': stock
    }
    return render(request, 'posApp/supplier_supplies.html', context)


@login_required
def dashboard_customersales(request, pk, pk1):
    user = Users.objects.get(email=pk)
    customer = Customer.objects.get(id=pk1)
    sales = CustomerSales.objects.filter(customer_id=pk1).order_by('-id')
    context = {
        'user': user,
        'customer': customer,
        'sales': sales
    }
    return render(request, 'posApp/customer_sales.html', context)


@login_required
def view_dash_customerinvoice(request, pk, pk1, pk2):
    user = Users.objects.get(email=pk)
    customers = Customer.objects.get(id=pk1)
    customer_sales = CustomerSales.objects.get(id=pk2)
    customer_sales_items = CustomerSalesItems.objects.filter(sale_id=pk2)
    grand_total = customer_sales.grand_total + customer_sales.tax_amount
    context = {
        'user': user,
        'customers': customers,
        'customer_sales': customer_sales,
        'customer_sales_items': customer_sales_items,
        'grand_total': grand_total
    }
    return render(request, 'docs/dashboardsale.html', context)


@login_required
def view_dash_supplyinvoice(request, pk, pk1, pk2):
    user = Users.objects.get(email=pk)
    supplier = Supplier.objects.get(id=pk1)
    stock = ProductChange.objects.get(id=pk2)
    supplied_items = changeItems.objects.filter(change_id_id=pk2)
    grand_total = stock.grand_total + stock.tax_amount
    context = {
        'user': user,
        'supplier': supplier,
        'stock': stock,
        'supplied_items': supplied_items,
        'grand_total': grand_total
    }
    return render(request, 'docs/dashboardsupplies.html', context)


@login_required
def view_supply_invoice(request, pk, pk1, pk2):
    branch = Branch.objects.get(id=pk)
    supplier = Supplier.objects.get(id=pk1)
    stock = ProductChange.objects.get(id=pk2)
    supplied_items = changeItems.objects.filter(change_id_id=pk2)
    grand_total = stock.grand_total + stock.tax_amount
    context = {
        'branch': branch,
        'supplier': supplier,
        'stock': stock,
        'supplied_items': supplied_items,
        'grand_total': grand_total
    }
    return render(request, 'docs/branchsupplies.html', context)


@login_required
def move_product(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    branches = Branch.objects.all()
    product_s = Products.objects.get(id=pk1)
    form = MoveForm(request.POST or None, request.FILES or None)
    context = {'branch': branch, 'branch1': branch1, 'products': product_s, 'branches': branches, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            move = form.save(commit=False)
            move.user = request.user
            move.product = product_s
            move.branch_owner = branch
            move.save()

            quantity_moved = move.qty

            product_s.stock = int(product_s.stock) - float(quantity_moved)
            product_s.save()

            updated_product = Products.objects.filter(branch_owner_id=move.branch_to)
            updated_product.filter(code=product_s.code).exists()
            print(updated_product)

            if updated_product:
                print('it exist in this branch too')
                stuff = Products.objects.filter(branch_owner_id=move.branch_to).get(code=product_s.code)
                print(stuff)
                updated = updated_product.filter(code=product_s.code).update(stock=move.qty + int(stuff.stock))

            else:
                product = Products.objects.create(code=product_s.code, category_id=product_s.category_id,
                                                  name=product_s.name,
                                                  description=product_s.description,
                                                  price=product_s.price, status=product_s.status,
                                                  branch_owner=move.branch_to,
                                                  stock=move.qty,
                                                  expiry_date=product_s.expiry_date, image=product_s.image)
                product.save()

            return render(request, 'posApp/movecomplete.html', {'branch': branch})
    else:
        form.fields["branch_from"].queryset = Branch.objects.filter(user=request.user)
        form.fields["branch_to"].queryset = Branch.objects.filter(user=request.user)
    return render(request, 'posApp/moveproduct.html', context=context)


@login_required
def lab_register(request, pk):
    users = Users.objects.get(email=pk)
    # user = Branch.objects.filter(user=request.user)
    user = Users.objects.all()
    context = {'user': user, 'users': users}
    if request.method == "POST":
        # form = BranchForm(request.POST or None)
        # branch = form
        lab_id = request.POST.get('labid')
        lab_name = request.POST.get('labname')
        # branch.location = request.POST['branchlocation']
        lab_phone = request.POST.get('phone')
        lab_user = request.POST.get('user1')
        lab = Lab.objects.create(id=lab_id, name=lab_name, location=None, phone=lab_phone)
        lab.user.add(lab_user or None)
        context['labid'] = lab
        context['created'] = True
    return render(request, 'labApp/labregister.html', context=context)


def labs(request, pk):
    user = Users.objects.get(email=pk)
    branch = Lab.objects.filter(user=pk)
    return render(request, 'labApp/labs.html', {'user': user, 'branch': branch})


@login_required
def homelab(request, pk):
    if request.user.is_authenticated:
        lab = Lab.objects.get(id=pk)
        now = datetime.now()
        current_year = now.strftime("%Y")
        current_month = now.strftime("%m")
        current_day = now.strftime("%d")
        investigations = len(Investigations.objects.filter(lab_owner_id=pk))
        context = {
            'page_title': 'Home',
            'investigations': investigations,
            'lab': lab
        }
        return render(request, 'labApp/labhome.html', context)
    else:
        return redirect('login-me')


@login_required
def investigations_list(request, pk):
    lab = Lab.objects.get(id=pk)
    investigations = Investigations.objects.filter(lab_owner_id=pk)
    context = {
        'lab': lab,
        'investigations': investigations,
    }

    return render(request, 'labApp/investigations.html', context)


@login_required
def new_investigation(request, pk):
    lab = Lab.objects.get(id=pk)
    form = InvestigationForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.lab_owner = lab
            # cat.user = request.user
            result.save()
            return render(request, 'labApp/confirmnewtest.html', {'lab': lab})
    else:
        return render(request, 'labApp/newinvestiagtion.html', context=context)


@login_required
def all_patients(request, pk):
    lab = Lab.objects.get(id=pk)
    patients = Patient.objects.filter(lab_owner_id=pk)
    context = {
        'lab': lab,
        'patients': patients,
    }
    return render(request, 'labApp/patients.html', context)


@login_required
def register_patient(request, pk):
    lab = Lab.objects.get(id=pk)
    context = {
        'lab': lab,
    }
    if request.method == "POST":
        # form = BranchForm(request.POST or None)
        # branch = form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # branch.location = request.POST['branchlocation']
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        email = request.POST.get('email')
        patient = Patient.objects.create(firstname=first_name or None, middlename=None, lastname=last_name or None,
                                         gender=gender or None, dob=dob or None, contact=contact or None,
                                         address=address or None, email=email or None, created_by=request.user,
                                         lab_owner=lab)
        context['patientid'] = patient
        context['created'] = True

    return render(request, 'labApp/newpatient.html', context=context)


@login_required
def patient(request, pk, pk1):
    if request.user.is_authenticated:
        lab = Lab.objects.get(id=pk)
        patient = Patient.objects.get(id=pk1)
        complaint = Complaint.objects.filter(patient_id=pk1).first()
        context = {
            'page_title': 'Home',
            'lab': lab,
            'patient': patient,
            'complaint': complaint
        }
        return render(request, 'labApp/patient_info.html', context)
    else:
        return redirect('login-me')


@login_required
def liver_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Liver_Function_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientliver_info.html', context)


@login_required
def renal_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Renal_Function_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientrenal_info.html', context)


@login_required
def pancreas_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Pancreatic_enzymes_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientpancreas_info.html', context)


@login_required
def iron_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Ironprofile_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientiron_info.html', context)


@login_required
def lipid_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = LipidProfile_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientlipid_info.html', context)


@login_required
def inflammatory_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Inflammtory_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientinflame_info.html', context)


@login_required
def ascetic_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Ascetic_Fluid_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientascetic_info.html', context)


@login_required
def electrolytes_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Elements_conc_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientions_info.html', context)


@login_required
def sugar_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Diabetic_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientsugar_info.html', context)


@login_required
def cardiac_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Cardiac_Markers.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientcardiac_info.html', context)


@login_required
def repro_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Reproduction.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientrepro_info.html', context)


@login_required
def autoimmunity_and_cancer_patient(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    investigations = Autoimmunity_and_cancer_Test.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'investigations': investigations,
    }
    return render(request, 'labApp/patientaac_info.html', context)


@login_required
def test_list(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    context = {'lab': lab, 'patient': patient}
    return render(request, 'labApp/choosetest.html', context)


@login_required
def liver_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = LiverForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/livertestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='L')
        return render(request, 'labApp/livertest.html', context=context)


@login_required
def liver_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Liver_Function_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/liverinfo.html', context)


@login_required
def renal_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = RenalForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/renaltestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='R')
        return render(request, 'labApp/renaltest.html', context=context)


@login_required
def renal_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Renal_Function_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/renalinfo.html', context)


@login_required
def pancreatic_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = PancreaticForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/pancreastestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='P')
        return render(request, 'labApp/pancreastest.html', context=context)


@login_required
def pancreas_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Pancreatic_enzymes_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/pancreasinfo.html', context)


@login_required
def ironprofile_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = IronForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/irontestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='Iron')
        return render(request, 'labApp/irontest.html', context=context)


@login_required
def iron_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Ironprofile_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/ironinfo.html', context)


@login_required
def lipidprofile_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = LipidForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/lipidtestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='Lipid')
        return render(request, 'labApp/lipidtest.html', context=context)


@login_required
def lipid_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = LipidProfile_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/lipidinfo.html', context)


@login_required
def inflammatory_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = InflammatoryForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/inflametestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='I')
        return render(request, 'labApp/inflammationtest.html', context=context)


@login_required
def inflammatory_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Inflammtory_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/inflameinfo.html', context)


@login_required
def ascetic_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = AsceticForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/ascetictestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='A')
        return render(request, 'labApp/ascetictest.html', context=context)


@login_required
def ascetic_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Ascetic_Fluid_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/asceticinfo.html', context)


@login_required
def electrolytes_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = ElectrolytesForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/ionstestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='E')
        return render(request, 'labApp/electrolytestest.html', context=context)


@login_required
def ions_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Elements_conc_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/ionsinfo.html', context)


@login_required
def sugar_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = DiabeticForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/sugartestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='D')
        return render(request, 'labApp/sugartest.html', context=context)


@login_required
def sugar_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Diabetic_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/sugarinfo.html', context)


@login_required
def cardiac_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = CardiacForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/cardiactestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='C')
        return render(request, 'labApp/cardiactest.html', context=context)


@login_required
def cardiac_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Cardiac_Markers.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/cardiacinfo.html', context)


@login_required
def reproductive_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = ReproductionForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/reprotestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='RP')
        return render(request, 'labApp/reprotest.html', context=context)


@login_required
def repro_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Reproduction.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/reproinfo.html', context)


@login_required
def auto_and_ca_test(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = AandCForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            result = form.save(commit=False)
            result.created_by = request.user
            result.patient = patient
            result.lab_owner = lab
            # cat.user = request.user

            result.save()

            result.investigation_request.set(form.cleaned_data['investigation_request'] or None)

            for test in result.investigation_request.all():
                saved_test = Test_performed.objects.create(name=test.name, price=test.cost, lab_owner=lab, created_by=request.user)

                saved_test.save()

            return render(request, 'labApp/aactestalert.html', {'lab': lab, 'patient': patient, 'result': result})
    else:
        form.fields["investigation_request"].queryset = Investigations.objects.filter(category='AaC')
        return render(request, 'labApp/aactest.html', context=context)


@login_required
def aac_info(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    results = Autoimmunity_and_cancer_Test.objects.get(id=pk2)
    context = {
        'lab': lab,
        'patient': patient,
        'results': results
    }
    return render(request, 'labApp/aacinfo.html', context)


@login_required
def new_complaint(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = ComplaintForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            complaint.patient = patient
            complaint.lab_owner = lab
            # cat.user = request.user

            complaint.save()

            return render(request, 'labApp/complaintaddedalert.html', {'lab': lab, 'patient': patient, 'complaint': complaint})
    else:
        return render(request, 'labApp/complaintform.html', context=context)


@login_required
def patient_prescriptions(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    prescriptions = Prescription.objects.filter(patient_id=pk1)
    context = {
        'lab': lab,
        'patient': patient,
        'prescriptions': prescriptions
    }
    return render(request, 'labApp/prescription.html', context=context)


@login_required
def new_prescription(request, pk, pk1):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    form = PrescriptionForm(request.POST or None, request.FILES or None)
    context = {'lab': lab, 'patient': patient, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.created_by = request.user
            prescription.patient = patient
            prescription.lab_owner = lab
            # cat.user = request.user

            prescription.save()

            return render(request, 'labApp/prescriptionaddedalert.html',
                          {'lab': lab, 'patient': patient, 'prescription': prescription})
    else:
        return render(request, 'labApp/prescriptionform.html', context=context)


@login_required
def update_prescription(request, pk, pk1, pk2):
    lab = Lab.objects.get(id=pk)
    patient = Patient.objects.get(id=pk1)
    show_prescription = Prescription.objects.get(id=pk2)
    form = PrescriptionForm(request.POST or None, request.FILES or None, instance=show_prescription)
    context = {'lab': lab, 'patient': patient, 'form': form, 'show_prescription': show_prescription}
    if form.is_valid():
        prescription = form.save(commit=False)
        prescription.created_by = request.user
        prescription.patient = patient
        prescription.lab_owner = lab
        # cat.user = request.user

        prescription.save()

        return render(request, 'labApp/prescriptionaddedalert.html',
                      {'lab': lab, 'patient': patient, 'prescription': prescription})

    return render(request, 'labApp/prescriptionupdateform.html', context=context)


@login_required
def all_testperformed(request, pk):
    lab = Lab.objects.get(id=pk)
    tests = Test_performed.objects.filter(lab_owner_id=pk)
    context = {
        'lab': lab,
        'tests': tests
    }
    return render(request, 'labApp/alltestperformed.html', context)