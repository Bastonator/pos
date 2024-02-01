from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic.base import RedirectView
from .forms import PwdResetForm, PwdResetConfirmForm


urlpatterns = [
    #path('redirect-admin', RedirectView.as_view(url="/admin"),name="redirect-admin"),
    path('', views.index, name='home'),
    path('branch_register/', views.branch_register, name='branchregister'),
    path('<str:pk>', views.home, name="home-page"),
    path('login/', views.login_account, name='login-me'),
    #path('login', auth_views.LoginView.as_view(template_name = 'posApp/login.html',redirect_authenticated_user=True), name="login"),
    #path('userlogin', views.login_user, name="login-user"),
    path('logout/', views.logoutuser, name="logout"),
    path('account_register/', views.account_register, name='account-register'),
    path('account/<str:pk>', views.user_account, name='user-dash'),
    path('branch_users/<str:pk>/<str:pk1>', views.branch_users, name="users"),
    path('delete_branch_users/<str:pk>/<str:pk1>', views.delete_branch_users, name="delete-user"),
    path('manage_branch/<str:pk>', views.manage_users, name="manage-branch"),
    path('add_cat/<str:pk>', views.addnew_cat, name="cat-add"),
    path('category/<str:pk>', views.category, name="category-page"),
    path('manage_category/<str:pk>', views.manage_category, name="manage_category-page"),
    path('save_category/<str:pk>', views.save_category, name="save-category-page"),
    path('delete_category/<str:pk>', views.delete_category, name="delete-category"),
    path('add_prod/<str:pk>', views.addnew_prod, name="prod-add"),
    path('products/<str:pk>', views.products, name="product-page"),
    path('manage_products/<str:pk>', views.manage_products, name="manage_products-page"),
    path('test', views.test, name="test-page"),
    path('save_product/<str:pk>', views.save_product, name="save-product-page"),
    path('delete_product/<str:pk>', views.delete_product, name="delete-product"),
    path('pos/<str:pk>', views.pos, name="pos-page"),
    path('checkout-modal/<str:pk>', views.checkout_modal, name="checkout-modal"),
    path('add_sale/<str:pk>', views.addnew_sale, name="sale-add"),
    path('save-pos/<str:pk>', views.save_pos, name="save-pos"),
    path('sales/<str:pk>', views.salesList, name="sales-page"),
    path('receipt/<str:pk>', views.receipt, name="receipt-modal"),
    path('delete_sale/<str:pk>', views.delete_sale, name="delete-sale"),
    path('inventory/<str:pk>', views.inventory, name="inventory"),
    path('todays_sales/<str:pk>', views.todays_sales, name="todays-sales"),
    path('todays_sales_items/<str:pk>', views.todays_sale_items, name="todays-sale_items"),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html",
                                              form_class=PwdResetForm),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html",
                                                     form_class=PwdResetConfirmForm),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
         name='password_reset_complete'),
    # path('employees', views.employees, name="employee-page"),
    # path('manage_employees', views.manage_employees, name="manage_employees-page"),
    # path('save_employee', views.save_employee, name="save-employee-page"),
    # path('delete_employee', views.delete_employee, name="delete-employee"),
    # path('view_employee', views.view_employee, name="view-employee-page"),
]