from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse
from flask import jsonify
from posApp.models import Category, Products, Sales, salesItems, Shifts, ProductChange, changeItems, Move
from django.db.models import Count, Sum
from posApp.models import Branch, Users
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import json, sys
from datetime import date, datetime
from posApp.forms import RegistrationForm, BranchForm, CategoryForm, ProductForm, SaleForm, MoveForm
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
    return redirect('home')


# Create your views here.
def index(request):
    return render(request, 'posApp/landingpage.html')


def user_account(request, pk):
    user = Users.objects.get(email=pk)
    branch = Branch.objects.filter(user=pk)
    return render(request, 'posApp/index.html', {'user': user, 'branch': branch})


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
    user = Users.objects.all()
    context = {'user': user, 'users': users}
    if request.method == "POST":
        # form = BranchForm(request.POST or None)
        # branch = form
        branch_id = request.POST.get('branchid')
        branch_name = request.POST.get('branchname')
        # branch.location = request.POST['branchlocation']
        branch_address = request.POST.get('branchaddress')
        branch_phone = request.POST.get('phone')
        branch_user = request.POST.get('user1')
        branch_user2 = request.POST.get('user2')
        branch_user3 = request.POST.get('user3')
        branch_user4 = request.POST.get('user4')
        branch_user5 = request.POST.get('user5')
        branch_user6 = request.POST.get('user6')
        branch = Branch.objects.create(id=branch_id, name=branch_name, location=None, address=branch_address, phone=branch_phone)
        branch.user.add(branch_user or None)
        # it is branch.user.add because user is how the many to many field is designated in the models.py
        branch.user.add(branch_user2 or None)
        branch.user.add(branch_user3 or None)
        branch.user.add(branch_user4 or None)
        branch.user.add(branch_user5 or None)
        branch.user.add(branch_user6 or None)
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
def products(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    product_list = Products.objects.filter(branch_owner_id=pk).order_by('name')
    context = {
        'page_title': 'Product List',
        'products': product_list,
        'branch': branch,
        'branch1': branch1,
    }
    return render(request, 'posApp/products.html', context)


@login_required
def manage_products(request, pk):
    branch = Branch.objects.get(id=pk)
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
        'branch': branch
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
                                                                             image=request.FILES['img'])
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
    sales = Sales.objects.filter(shift_sold_id=pk1)
    #did't work till i added sale data and made the data render in a list format. ofcourse i appeded the data at the end.
    sale_data = []

    for sale in sales:
        item = sale
        for prod in salesItems.objects.filter(sale_id=item).order_by('id'):
            print(prod)
            stuff = prod
            sale_data.append(stuff)
            context = {
                'branch': branch,
                'branch1': branch1,
                'shift': shift,
                'sales': sales,
                'sale_data': sale_data
            }

        total = 0

        for sale in sales:
            total = total + sale.grand_total
            print(total)

        shift.shift_sales = total
        #data = salesItems.objects.filter(sale_id=item)
    return render(request, 'posApp/shiftsaleitems.html', context)

@login_required
def pos(request, pk):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
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
    context = {
        'page_title': 'Sales Transactions',
        'sale_data': sale_data,
        'branch': branch,
        'branch1': branch1,
        'sales': sales
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
        change = ProductChange(code=code, sub_total=data['sub_total'], tax=data['tax'], tax_amount=data['tax_amount'],
                      grand_total=data['grand_total'], tendered_amount=data['tendered_amount'],
                      amount_change=data['amount_change'], branch_owner=branch, user=request.user).save()
        change_id = ProductChange.objects.last().pk
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod
            change = ProductChange.objects.filter(id=change_id).first()
            product = Products.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i]
            price = data.getlist('cost_price[]')[i]
            supplier = data.getlist('supplier')[i]
            new_costprice = data.getlist('new_cost')[i]
            total = float(qty) * float(price)
            product.stock = product.stock + float(qty)
            product.supplier = supplier
            product.cost_price = new_costprice
            product.save()
            print({'change_id': change, 'product_id': product, 'qty': qty, 'price': price, 'total': total})
            changeItems(change_id=change, product_id=product, qty=qty, price=price, total=total, branch_owner=branch).save()
            i += int(1)
        resp['status'] = 'success'
        resp['change_id'] = change_id
        messages.success(request, "Stock has been added.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
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
def move_product(request, pk, pk1):
    branch = Branch.objects.get(id=pk)
    branch1 = Branch.objects.get(id=pk)
    branches = Branch.objects.all()
    products = Products.objects.get(id=pk1)
    form = MoveForm(request.POST or None, request.FILES or None)
    context = {'branch': branch, 'branch1': branch1, 'products': products, 'branches': branches, 'form': form}
    if request.method == "POST":
        print(form)
        if form.is_valid():
            move = form.save(commit=False)
            move.user = request.user
            move.product = products
            move.branch_owner = branch
            move.save()

            quantity_moved = move.qty

            products.stock = int(products.stock) - float(quantity_moved)
            products.save()

            product = Products.objects.create(code=products.code, category_id=products.category_id, name=products.name,
                                              description=products.description,
                                              price=products.price, status=products.status, branch_owner=move.branch_to,
                                              stock=move.qty,
                                              expiry_date=products.expiry_date, image=products.image)
            product.save()

            return render(request, 'posApp/movecomplete.html', {'branch': branch})
    else:
        form.fields["branch_from"].queryset = Branch.objects.filter(user=request.user)
        form.fields["branch_to"].queryset = Branch.objects.filter(user=request.user)
        form.fields["branch_owner"].queryset = Branch.objects.filter(user=request.user)
    return render(request, 'posApp/moveproduct.html', context=context)