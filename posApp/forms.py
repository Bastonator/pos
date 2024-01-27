from django import forms
from django.forms.models import ModelForm
from .models import Users, Branch, Category, Products, Sales
from django_countries.fields import CountryField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Enter Username', min_length=1, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required',
                             error_messages={'required': 'Sorry, you will need an email'})
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)
    phone_number = forms.IntegerField(label='Enter Phone Number', help_text='Required')

    class Meta:
        model = Users
        fields = ('username', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Users.objects.filter(username=username)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError("Sorry, the passwords don't match")
        return cd['password1']

    # def clean_password2(self):
    # cd = self.cleaned_data
    # if cd['password'] != cd['password2']:
    # raise forms.ValidationError('Passwords do not match.')
    # return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if Users.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                'Please use another Phone number, that is already taken')
        return phone_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'phone_number'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, user):
        return '%s' % user.name


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'location', 'phone', 'user')
        user = CustomMMCF(queryset=Users.objects.all(), widget=forms.CheckboxSelectMultiple(
            # attrs={'class': 'form-check-input'}
        ))

        labels = {
            'id': 'Branch ID',
            'name': 'Branch Name',
            'location': 'Branch Country',
            'phone': 'Branch Phone number',
            'user': 'Which user will operate this branch.'
        }

        widgets = {
            'id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Link name. Note: make sure there are no spaces.'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch name'}),
            'location': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose your country'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number.'}),
            'user': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}), }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description', 'status', 'branch_owner')

        labels = {
            'name': 'Category name',
            'description': 'Description',
            'branch_owner': 'Branch',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cat name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Description'}),
            'branch_owner': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ('code', 'category_id', 'name', 'description', 'price', 'status', 'branch_owner', 'stock')

        labels = {
            'code': '',
            'category_id': '',
            'name': 'Category name',
            'description': 'Description',
            'price': 'Price',
            'branch_owner': 'Branch',
            'stock': '',
        }

        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'category_id': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prod name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Description'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'branch_owner': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'stock': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'in stock'}),
        }


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = (
        'code', 'sub_total', 'grand_total', 'tax_amount', 'tax', 'tendered_amount', 'branch_owner', 'amount_change')

        labels = {
            'code': '',
            'sub_total': '',
            'grand_total': 'Category name',
            'tax_amount': 'Description',
            'tax': 'Price',
            'branch_owner': 'Branch',
            'tendered_amount': '',
            'amount_change': '',
        }

        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code'}),
            'sub_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'grand_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prod name'}),
            'tax_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Description'}),
            'tax': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'branch_owner': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'tendered_amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'in stock'}),
            'amount_change': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'in stock'}),
        }