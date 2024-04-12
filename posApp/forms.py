from django import forms
from django.forms.models import ModelForm
from .models import Users, Branch, Category, Products, Prescription, Sales, Move, Lab, Patient, Pancreatic_enzymes_Test, Ironprofile_Test, LipidProfile_Test, Reproduction, Ascetic_Fluid_Test, Autoimmunity_and_cancer_Test, Inflammtory_Test, Diabetic_Test, Renal_Function_Test, Cardiac_Markers, Investigations, Liver_Function_Test, Elements_conc_Test, Complaint, Customer, Supplier
from django_countries.fields import CountryField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm


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


##class CustomMMCF(forms.ModelMultipleChoiceField):
    ###def label_from_instance(self, user):
        ###return '%s' % user.name
    ###


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'location', 'phone')
        #user = CustomMMCF(queryset=Users.objects.all(), widget=forms.CheckboxSelectMultiple(
            # attrs={'class': 'form-check-input'}
        #))

        labels = {
            'id': 'Branch ID',
            'name': 'Branch Name',
            'location': 'Branch Country',
            'phone': 'Branch Phone number',
        }

        widgets = {
            'id': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Link name. Note: make sure there are no spaces.'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Branch name'}),
            'location': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose your country'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number.'}),
        }


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



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'address', 'phone', 'email', 'branch_owner')

        labels = {
            'name': '',
            'address': '',
            'phone': '',
            'email': '',
            'branch_owner': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company/Customer name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customers address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customers Email'}),
            'branch_owner': forms.CheckboxSelectMultiple()
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('id', 'name', 'address', 'phone', 'email', 'branch_owner')

        labels = {
            'id': '',
            'name': '',
            'address': '',
            'phone': '',
            'email': '',
            'branch_owner': '',
        }
        widgets = {
            'id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier unique Id'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company/Supplier name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customers address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customers Email'}),
            'branch_owner': forms.CheckboxSelectMultiple()
        }


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        e = Users.objects.filter(email=email)
        if not e:
            raise forms.ValidationError(
                "Sorry there is an error, try again"
            )
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'New password'}))
    new_password2 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'New password'}))

    def clean_new_password2(self):
        cnd = self.cleaned_data
        if cnd['new_password1'] != cnd['new_password2']:
            raise forms.ValidationError("Sorry, the passwords you entered don't match")
        return cnd['new_password1']


class MoveForm(forms.ModelForm):
    class Meta:
        model = Move
        fields = ('branch_from', 'branch_to', 'qty')

        labels = {
            'branch_from': '',
            'branch_to': '',
            'qty': ''
        }

        widgets = {
            'branch_from': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'branch_to': forms.Select(attrs={'class': 'form-control', 'placeholder': ''}),
            'qty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'How much are you sending?'})
        }


class LiverForm(forms.ModelForm):
    class Meta:
        model = Liver_Function_Test
        fields = (
        'investigation_request', 'alanine_transferase', 'albumin', 'ALP', 'aspartate_transferase', 'Bilirubin_direct',
        'Bilirubin_total', 'GGT', 'Globin', 'total_protein', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'alanine_transferase': '',
            'albumin': '',
            'ALP': '',
            'aspartate_transferase': '',
            'Bilirubin_direct': '',
            'Bilirubin_total': '',
            'GGT': '',
            'Globin': '',
            'total_protein': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'alanine_transferase': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'alanine_transferase'}),
            'albumin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'albumin'}),
            'ALP': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ALP'}),
            'aspartate_transferase': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'aspartate_transferase'}),
            'Bilirubin_direct': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bilirubin_direct'}),
            'Bilirubin_total': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bilirubin_total'}),
            'GGT': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GGT'}),
            'Globin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Globin'}),
            'total_protein': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'total_protein'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class InvestigationForm(forms.ModelForm):
    class Meta:
        model = Investigations
        fields = ('name', 'cost', 'category')

        TESTS = [
            ('L', 'Liver Function Test'),
            ('P', 'Pancreatic Enzymes Test'),
        ]

        labels = {
            'name': '',
            'cost': '',
            'category': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of investigation'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price of test'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class RenalForm(forms.ModelForm):
    class Meta:
        model = Renal_Function_Test
        fields = ('investigation_request', 'creatinine', 'urea', 'onedayGFR', 'onedayprotein', 'onedaycreatinine', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'creatinine': '',
            'urea': '',
            'onedayGFR': '',
            'onedayprotein': '',
            'onedaycreatinine': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'creatinine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Creatinine conc.'}),
            'urea': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Urea conc.'}),
            'onedayGFR': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '24hr GFR'}),
            'onedayprotein': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '24hr Protein'}),
            'onedaycreatinine': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '24hr Creatinine'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class PancreaticForm(forms.ModelForm):
    class Meta:
        model = Pancreatic_enzymes_Test
        fields = ('investigation_request', 'Amylase', 'Lipase', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'Amylase': '',
            'Lipase': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'Amylase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amylase conc.'}),
            'Lipase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lipase conc.'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),

        }


class AsceticForm(forms.ModelForm):
    class Meta:
        model = Ascetic_Fluid_Test
        fields = ('investigation_request', 'Total_protein', 'Albumin', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'Total_protein': '',
            'Albumin': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'Total_protein': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asctic Protein conc.'}),
            'Albumin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asctic Albumin'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class InflammatoryForm(forms.ModelForm):
    class Meta:
        model = Inflammtory_Test
        fields = ('investigation_request', 'AFP', 'CRP', 'Anti_ccp', 'RF_IgM', 'RA_or_F', 'Uric_acid', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'AFP': '',
            'CRP': '',
            'Anti_ccp': '',
            'RF_IgM': '',
            'RA_or_F': '',
            'Uric_acid': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'AFP': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Alfa-fetoprotein conc.'}),
            'CRP': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'C-Reactive Protein conc.'}),
            'Anti_ccp': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Antibody for Cyclic Citrullinated Peptide(Anti CCP)'}),
            'RF_IgM': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Rheumatoid factor Immunoglobulin M'}),
            'RA_or_F': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Rheumatoid arthritis/Rheumatoid factor'}),
            'Uric_acid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Uric acid conc.'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class IronForm(forms.ModelForm):
    class Meta:
        model = Ironprofile_Test
        fields = ('investigation_request', 'Ferritin', 'Iron', 'Total_IBC', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'Ferritin': '',
            'Iron': '',
            'Total_IBC': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'Ferritin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ferritin conc.'}),
            'Iron': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Iron conc.'}),
            'Total_IBC': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Iron Bindin Capacity'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class LipidForm(forms.ModelForm):
    class Meta:
        model = LipidProfile_Test
        fields = ('investigation_request', 'HDL', 'LDL', 'Total_cholesterol', 'TG', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'HDL': '',
            'LDL': '',
            'Total_cholesterol': '',
            'TG': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'HDL': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cholesterol HDL'}),
            'LDL': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cholesterol LDL'}),
            'Total_cholesterol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Cholesterol'}),
            'TG': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Triglyceride'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class ElectrolytesForm(forms.ModelForm):
    class Meta:
        model = Elements_conc_Test
        fields = (
        'investigation_request', 'phosphorus', 'magnesium', 'calcium', 'sodium', 'potassium', 'bicarbonate', 'hydrogen',
        'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'phosphorus': '',
            'magnesium': '',
            'calcium': '',
            'sodium': '',
            'potassium': '',
            'bicarbonate': '',
            'hydrogen': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'phosphorus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phosphorus ion conc.'}),
            'magnesium': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Magnesium ion conc.'}),
            'calcium': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calcium ion conc.'}),
            'sodium': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sodium ion conc.'}),
            'potassium': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Potassium ion conc.'}),
            'bicarbonate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bicarbonate ion conc.'}),
            'hydrogen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hydorgen ion conc.'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class DiabeticForm(forms.ModelForm):
    class Meta:
        model = Diabetic_Test
        fields = (
        'investigation_request', 'HBA1C', 'RBG', 'FBG', 'microalbumin', 'insulin', 'serum_glucose', 'oral_glucose',
        'c_pepetide', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'HBA1C': '',
            'RBG': '',
            'FBG': '',
            'microalbumin': '',
            'insulin': '',
            'serum_glucose': '',
            'oral_glucose': '',
            'c_pepetide': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'HBA1C': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Haemoglobin A1Cconc.'}),
            'RBG': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Random blood glucose'}),
            'FBG': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fasting blood glucose'}),
            'microalbumin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Urine Microalbumin conc.'}),
            'insulin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insulin conc.'}),
            'serum_glucose': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serum glucose'}),
            'oral_glucose': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serum Oral glucose'}),
            'c_pepetide': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'C-Peptide conc.'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class CardiacForm(forms.ModelForm):
    class Meta:
        model = Cardiac_Markers
        fields = ('investigation_request', 'NT_pro_BNP', 'D_dimer', 'calcium', 'troponin_1', 'CK', 'LDH', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'NT_pro_BNP': '',
            'D_dimer': '',
            'calcium': '',
            'troponin_1': '',
            'CK': '',
            'LDH': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'NT_pro_BNP': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Natriuretic peptide conc.'}),
            'D_dimer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'D-Dimer'}),
            'calcium': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calcium conc.'}),
            'troponin_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cardiac Troponin 1'}),
            'CK': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Creatine Kinase '}),
            'LDH': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lactate Dehydrogenase conc.'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class ReproductionForm(forms.ModelForm):
    class Meta:
        model = Reproduction
        fields = (
        'investigation_request', 'beta_HCG', 'urine_HCG', 'estradiol', 'FSH', 'Progesterone', 'LH', 'prolactin', 'AMH',
        'Testosterone', 'total_T4', 'total_t3', 'TSH', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'beta_HCG': '',
            'urine_HCG': '',
            'estradiol': '',
            'FSH': '',
            'Progesterone': '',
            'LH': '',
            'prolactin': '',
            'AMH': '',
            'Testosterone': '',
            'total_T4': '',
            'total_t3': '',
            'TSH': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'beta_HCG': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serum beta HCG.'}),
            'urine_HCG': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Urine HCG'}),
            'estradiol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serum Estradiol'}),
            'FSH': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Follicle stimulating hormone'}),
            'Progesterone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Progesterone'}),
            'LH': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Luteinizing hormone'}),
            'prolactin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prolactin'}),
            'AMH': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Anti-Mullerian Hormone'}),
            'Testosterone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Testosterone'}),
            'total_T4': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Thyroxine'}),
            'total_t3': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Total Triiodothyronine'}),
            'TSH': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thyroid stimulating hormone'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class AandCForm(forms.ModelForm):
    class Meta:
        model = Autoimmunity_and_cancer_Test
        fields = ('investigation_request', 'ANA', 'CA_125', 'CA15_3', 'CA19_9', 'CEA', 'PSA', 'confirmed_diagnosis')

        labels = {
            'investigation_request': '',
            'ANA': '',
            'CA_125': '',
            'CA15_3': '',
            'CA19_9': '',
            'CEA': '',
            'PSA': '',
            'confirmed_diagnosis': ''
        }

        widgets = {
            'investigation_request': forms.CheckboxSelectMultiple(),
            'ANA': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serum Antinuclear Antibodies'}),
            'CA_125': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Cancer antigen 125 for Ovarian cancer'}),
            'CA15_3': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Cancer antigen 15-3 for Breast cancer (increases in Non-cancerous conditions)'}),
            'CA19_9': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Cancer antigen 19-9 for Pancreatic Cancer'}),
            'CEA': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Carcinembryonic antigen for Colon cancer'}),
            'PSA': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prostatic specific antigen'}),
            'confirmed_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Querying Diagnosis'}),
        }


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('complaint1', 'complaint2', 'complaint3', 'complaint4', 'query_diagnosis')

        labels = {
            'complaint1': '',
            'complaint2': '',
            'complaint3': '',
            'complaint4': '',
            'query_diagnosis': ''
        }

        widgets = {
            'complaint1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patients Complaints, and Symptoms'}),
            'complaint2': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Patients Complaints, and Symptoms'}),
            'complaint3': forms.TextInput(attrs={'class': 'form-control',
                                             'placeholder': 'Patients Complaints, and Symptoms'}),
            'complaint4': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Patients Complaints, and Symptoms'}),
            'query_diagnosis': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Differential Diagnosis'}),
        }


class PrescriptionForm(forms.ModelForm):
    is_taking: forms.BooleanField()
    class Meta:
        model = Prescription
        fields = ('drug', 'dosage', 'is_taking')

        labels = {
            'drug': '',
            'dosage': '',
            'is_taking': ''
        }

        widgets = {
            'drug': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Drug prescribed'}),
            'dosage': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Dosage'}),
        }