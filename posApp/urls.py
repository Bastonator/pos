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
    path('branch_register/<str:pk>', views.branch_register, name='branchregister'),
    path('<str:pk>', views.home, name="home-page"),
    path('login/', views.login_account, name='login-me'),
    #path('login', auth_views.LoginView.as_view(template_name = 'posApp/login.html',redirect_authenticated_user=True), name="login"),
    #path('userlogin', views.login_user, name="login-user"),
    path('logout/', views.logoutuser, name="logout"),
    path('account_register/', views.account_register, name='account-register'),
    path('account/<str:pk>', views.user_account, name='user-dash'),
    path('branches/<str:pk>', views.branches, name='branch-dash'),
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
    path('shift/<str:pk>', views.shift_list, name="shift"),
    path('start_shift/<str:pk>', views.start_shift, name="start-shift"),
    path('shift_sales/<str:pk>/<str:pk1>', views.shift_sales, name="shift-sales"),
    path('shift_sale_items/<str:pk>/<str:pk1>', views.shift_sale_items, name="shift-sale-items"),
    path('product_change/<str:pk>', views.product_change, name="change-page"),
    path('change_modal/<str:pk>', views.change_modal, name="checkout-modal-change"),
    path('save_change/<str:pk>', views.save_change, name="save-change"),
    path('receipt_change/<str:pk>', views.receipt_forstock, name="receipt-modal-change"),
    path('move_product/<str:pk>/<str:pk1>', views.move_product, name="move-product"),
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

    path('lab_register/<str:pk>', views.lab_register, name='labregister'),
    path('lab/<str:pk>', views.homelab, name="home-page-lab"),
    path('lab-list/<str:pk>', views.labs, name='lab-dash'),
    path('patients/<str:pk>', views.all_patients, name="patient-page"),
    path('register_patient/<str:pk>', views.register_patient, name="register-patient"),
    path('patient_info/<str:pk>/<str:pk1>', views.patient, name="patient"),
    path('add_investigation/<str:pk>', views.new_investigation, name="new-investigation"),
    path('investigations/<str:pk>', views.investigations_list, name="investigations"),
    path('liver_function_history/<str:pk>/<str:pk1>', views.liver_patient, name="liver-patient"),
    path('renal_function_history/<str:pk>/<str:pk1>', views.renal_patient, name="renal-patient"),
    path('pancreatic_enzymes_test_history/<str:pk>/<str:pk1>', views.pancreas_patient, name="pancreas-patient"),
    path('ironprofile_test_history/<str:pk>/<str:pk1>', views.iron_patient, name="iron-patient"),
    path('lipidprofile_test_history/<str:pk>/<str:pk1>', views.lipid_patient, name="lipid-patient"),
    path('inflammation_test_history/<str:pk>/<str:pk1>', views.inflammatory_patient, name="inflame-patient"),
    path('ascetic_fluid_test_history/<str:pk>/<str:pk1>', views.ascetic_patient, name="ascetic-patient"),
    path('electrolytes_test_history/<str:pk>/<str:pk1>', views.electrolytes_patient, name="ions-patient"),
    path('sugar_test_history/<str:pk>/<str:pk1>', views.sugar_patient, name="sugar-patient"),
    path('cardiac_markers_test_history/<str:pk>/<str:pk1>', views.cardiac_patient, name="cardiac-patient"),
    path('reproductive_test_history/<str:pk>/<str:pk1>', views.repro_patient, name="repro-patient"),
    path('autoimmunity_and_cancer_Test_test_history/<str:pk>/<str:pk1>', views.autoimmunity_and_cancer_patient, name="aac-patient"),

    path('liver_function_test/<str:pk>/<str:pk1>', views.liver_test, name="liver-test"),
    path('choose_test/<str:pk>/<str:pk1>', views.test_list, name="test-list"),
    path('renal_function_test/<str:pk>/<str:pk1>', views.renal_test, name="renal-test"),
    path('pancreatic_enzymes_test/<str:pk>/<str:pk1>', views.pancreatic_test, name="pancreas-test"),
    path('ironprofile_test/<str:pk>/<str:pk1>', views.ironprofile_test, name="iron-test"),
    path('lipidprofile_test/<str:pk>/<str:pk1>', views.lipidprofile_test, name="lipid-test"),
    path('inflammation_test/<str:pk>/<str:pk1>', views.inflammatory_test, name="inflame-test"),
    path('ascetic_fluid_test/<str:pk>/<str:pk1>', views.ascetic_test, name="ascetic-test"),
    path('electrolytes_test/<str:pk>/<str:pk1>', views.electrolytes_test, name="ions-test"),
    path('sugar_test/<str:pk>/<str:pk1>', views.sugar_test, name="sugar-test"),
    path('cardiac_markers_test/<str:pk>/<str:pk1>', views.cardiac_test, name="cardiac-test"),
    path('reproductive_test/<str:pk>/<str:pk1>', views.reproductive_test, name="repro-test"),
    path('autoimmunity_and_cancer_Test_test/<str:pk>/<str:pk1>', views.auto_and_ca_test, name="aac-test"),

    path('liver_result/<str:pk>/<str:pk1>/<str:pk2>', views.liver_info, name="liver-result"),
    path('renal_result/<str:pk>/<str:pk1>/<str:pk2>', views.renal_info, name="renal-result"),
    path('pancreas_result/<str:pk>/<str:pk1>/<str:pk2>', views.pancreas_info, name="pancreas-result"),
    path('iron_result/<str:pk>/<str:pk1>/<str:pk2>', views.iron_info, name="iron-result"),
    path('lipid_result/<str:pk>/<str:pk1>/<str:pk2>', views.lipid_info, name="lipid-result"),
    path('inflammatory_result/<str:pk>/<str:pk1>/<str:pk2>', views.inflammatory_info, name="inflame-result"),
    path('ascetic_result/<str:pk>/<str:pk1>/<str:pk2>', views.ascetic_info, name="ascetic-result"),
    path('ions_result/<str:pk>/<str:pk1>/<str:pk2>', views.ions_info, name="ions-result"),
    path('sugar_result/<str:pk>/<str:pk1>/<str:pk2>', views.sugar_info, name="sugar-result"),
    path('cardiac_result/<str:pk>/<str:pk1>/<str:pk2>', views.cardiac_info, name="cardiac-result"),
    path('repro_result/<str:pk>/<str:pk1>/<str:pk2>', views.repro_info, name="repro-result"),
    path('autoimmunity_and_cancer_Test_result/<str:pk>/<str:pk1>/<str:pk2>', views.repro_info, name="aac-result"),

    path('complaints/<str:pk>/<str:pk1>', views.new_complaint, name="complaint"),
    path('prescriptions/<str:pk>/<str:pk1>', views.patient_prescriptions, name="prescription"),
    path('prescribe/<str:pk>/<str:pk1>', views.new_prescription, name="add-prescription"),
    path('edit_prescription/<str:pk>/<str:pk1>/<str:pk2>', views.update_prescription, name="edit-prescription"),
    path('test_sales/<str:pk>', views.all_testperformed, name="all-testperformed"),

]