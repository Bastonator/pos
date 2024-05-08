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
    email = models.EmailField(blank=True, null=True)
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

class Customer(models.Model):
    name = models.TextField()
    address = models.CharField(max_length=555, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    branch_owner = models.ManyToManyField(Branch, related_name='branchcustomers', null=True)
    created_by = models.ForeignKey(Users, null=True, related_name='customercreator', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True, auto_created=False)
    name = models.TextField(null=True, blank=True)
    location = CountryField(null=True, blank=True)
    address = models.CharField(max_length=555, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    branch_owner = models.ManyToManyField(Branch, null=True, related_name='branchsuppliers')
    created_by = models.ForeignKey(Users, null=True, related_name='suppliercreator', on_delete=models.CASCADE)

    def __str__(self):
        return self.id


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
    cost_price = models.FloatField(default=0, null=True, blank=True)
    status = models.IntegerField(default=1)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='productsbranch', on_delete=models.CASCADE)
    stock = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    supplier = models.TextField(null=True, max_length=188, blank=True)
    suppliers = models.ForeignKey(Supplier, null=True, related_name='supplierbranch', on_delete=models.DO_NOTHING, blank=True)
    #user = models.ForeignKey(Users, related_name="products", on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return self.code + " - " + self.name


class ProductChange(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='changebranch', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, null=True, related_name='changesuser', on_delete=models.CASCADE)
    suppliers = models.ForeignKey(Supplier, null=True, related_name='supplierchangeproduct', on_delete=models.DO_NOTHING, blank=True)

    def __str__(self):
        return self.code


class Move(models.Model):
    branch_from = models.ForeignKey(Branch, related_name='movefrom', null=True, on_delete=models.DO_NOTHING)
    branch_to = models.ForeignKey(Branch, related_name='moveto', null=True, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Users, null=True, related_name='movingsuser', on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    qty = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now, null=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='movebranch', on_delete=models.CASCADE)


class changeItems(models.Model):
    change_id = models.ForeignKey(ProductChange,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now, null=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='changeitembranch', on_delete=models.CASCADE)


class Shifts(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(Users, null=True, related_name='shiftuser', on_delete=models.CASCADE)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='shiftbranch', on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)
    shift_sales = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shift-sales", kwargs={"pk": self.pk})


class Lab(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True, auto_created=False)
    name = models.CharField(max_length=100, null=True)
    user = models.ManyToManyField(Users, related_name='labusers')
    phone = models.IntegerField(null=True, blank=True)
    location = CountryField(null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.id


class Investigations(models.Model):
    TESTS = [
        ('L', 'Liver Function Test'),
        ('P', 'Pancreatic Enzymes Test'),
        ('R', 'Renal Function Test'),
        ('A', 'Ascetic Fluid Test'),
        ('I', 'Inflammatory Test'),
        ('Iron', 'Iron Profile Test'),
        ('Lipid', 'Lipid Profile Test'),
        ('E', 'Ions and Electrolyes Test'),
        ('D', 'Diabetic Test'),
        ('C', 'Cardiac Markers Test'),
        ('RP', 'Reproductive Test'),
        ('AaC', 'Autoimmunity and Cancer Test'),
        ('Misc', 'Ungrouped or miscellaneous Test'),
        ('Infect', 'Infections Test'),
        ('M', 'Microbiology Test'),
        ('Coa', 'Coagulation Profile Test'),
    ]
    name = models.CharField(max_length=100, null=True)
    created_by = models.ForeignKey(Users, related_name="investigation", on_delete=models.DO_NOTHING, null=True)
    cost = models.IntegerField(default=0)
    category = models.CharField(max_length=10, choices=TESTS, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labinvestigations', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Test_performed(models.Model):
    name = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="testsperformer", on_delete=models.DO_NOTHING, null=True)
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labtestperformed', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Patient(models.Model):
    firstname = models.TextField(blank=True, null=True)
    middlename = models.TextField(blank=True, null=True)
    lastname = models.TextField(blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    contact = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    created_by = models.ForeignKey(Users, related_name="patients", on_delete=models.DO_NOTHING, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labpatient', on_delete=models.CASCADE)

    def __str__(self):
        return self.firstname


class Complaint(models.Model):
    complaint1 = models.TextField(blank=True, null=True)
    complaint2 = models.TextField(blank=True, null=True)
    complaint3 = models.TextField(blank=True, null=True)
    complaint4 = models.TextField(blank=True, null=True)
    query_diagnosis = models.TextField(max_length=4500, blank=True, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientcomplaint")
    created_by = models.ForeignKey(Users, related_name="complaint", on_delete=models.DO_NOTHING, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labcomplaint', on_delete=models.CASCADE)

    def __str__(self):
        return self.query_diagnosis


class Prescription(models.Model):
    drug = models.TextField(blank=True, null=True)
    dosage = models.TextField(blank=True, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientprescription")
    is_taking = models.BooleanField(default=True)
    created_by = models.ForeignKey(Users, related_name="prescription", on_delete=models.DO_NOTHING, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labprescription', on_delete=models.CASCADE)

    def __str__(self):
        return self.drug



class Liver_Function_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="livertest")
    alanine_transferase = models.TextField(max_length=450, null=True, blank=True)
    albumin = models.TextField(max_length=450, null=True, blank=True)
    ALP = models.TextField(max_length=450, null=True, blank=True)
    aspartate_transferase = models.TextField(max_length=450, null=True, blank=True)
    Bilirubin_direct = models.TextField(max_length=450, null=True, blank=True)
    Bilirubin_total = models.TextField(max_length=450, null=True, blank=True)
    GGT = models.TextField(max_length=450, null=True, blank=True)
    Globin = models.TextField(max_length=450, null=True, blank=True)
    total_protein = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="liverlab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientliver")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labliver', on_delete=models.CASCADE)


class Renal_Function_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="renaltest")
    creatinine = models.TextField(max_length=450, null=True, blank=True)
    urea = models.TextField(max_length=450, null=True, blank=True)
    onedayGFR = models.TextField(max_length=450, null=True, blank=True)
    onedayprotein = models.TextField(max_length=450, null=True, blank=True)
    onedaycreatinine = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="renallab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientrenal")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labrenal', on_delete=models.CASCADE)


class Pancreatic_enzymes_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="pancreasetest")
    Amylase = models.TextField(max_length=450, null=True, blank=True)
    Lipase = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="pancreaselab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientpancreas")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labpancreas', on_delete=models.CASCADE)


class Ascetic_Fluid_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="ascetictest")
    Total_protein = models.TextField(max_length=450, null=True, blank=True)
    Albumin = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="asceticlab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientascetic")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labascetic', on_delete=models.CASCADE)


class Inflammtory_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="inflammationtest")
    AFP = models.TextField(max_length=450, null=True, blank=True)
    CRP = models.TextField(max_length=450, null=True, blank=True)
    Anti_ccp = models.TextField(max_length=450, null=True, blank=True)
    RF_IgM = models.TextField(max_length=450, null=True, blank=True)
    RA_or_F = models.TextField(max_length=450, null=True, blank=True)
    Uric_acid = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="inflammationlab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientinflammation")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labinflammation', on_delete=models.CASCADE)


class Ironprofile_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="irontest")
    Ferritin = models.TextField(max_length=450, null=True, blank=True)
    Iron = models.TextField(max_length=450, null=True, blank=True)
    Total_IBC = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="ironlab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientiron")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labiron', on_delete=models.CASCADE)


class LipidProfile_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="lipidtest")
    HDL = models.TextField(max_length=450, null=True, blank=True)
    LDL = models.TextField(max_length=450, null=True, blank=True)
    Total_cholesterol = models.TextField(max_length=450, null=True, blank=True)
    TG = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="lipidlab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientlipid")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='lablipid', on_delete=models.CASCADE)


class Elements_conc_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="elementstest")
    phosphorus = models.TextField(max_length=450, null=True, blank=True)
    magnesium = models.TextField(max_length=450, null=True, blank=True)
    calcium = models.TextField(max_length=450, null=True, blank=True)
    sodium = models.TextField(max_length=450, null=True, blank=True)
    potassium = models.TextField(max_length=450, null=True, blank=True)
    bicarbonate = models.TextField(max_length=450, null=True, blank=True)
    hydrogen = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="elementslab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientelements")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labelements', on_delete=models.CASCADE)


class Diabetic_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="diabetictest")
    HBA1C = models.TextField(max_length=450, null=True, blank=True)
    RBG = models.TextField(max_length=450, null=True, blank=True)
    FBG = models.TextField(max_length=450, null=True, blank=True)
    microalbumin = models.TextField(max_length=450, null=True, blank=True)
    insulin = models.TextField(max_length=450, null=True, blank=True)
    serum_glucose = models.TextField(max_length=450, null=True, blank=True)
    oral_glucose = models.TextField(max_length=450, null=True, blank=True)
    c_pepetide = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="diabeticslab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientdiabetic")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labdiabetic', on_delete=models.CASCADE)


class Cardiac_Markers(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="cardiactest")
    NT_pro_BNP = models.TextField(max_length=450, null=True, blank=True)
    D_dimer = models.TextField(max_length=450, null=True, blank=True)
    calcium = models.TextField(max_length=450, null=True, blank=True)
    troponin_1 = models.TextField(max_length=450, null=True, blank=True)
    CK = models.TextField(max_length=450, null=True, blank=True)
    LDH = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="cardiaclab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientcardiac")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labcardiac', on_delete=models.CASCADE)


class Reproduction(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="reprotest")
    beta_HCG = models.TextField(max_length=450, null=True, blank=True)
    urine_HCG = models.TextField(max_length=450, null=True, blank=True)
    estradiol = models.TextField(max_length=450, null=True, blank=True)
    FSH = models.TextField(max_length=450, null=True, blank=True)
    Progesterone = models.TextField(max_length=450, null=True, blank=True)
    LH = models.TextField(max_length=450, null=True, blank=True)
    prolactin = models.TextField(max_length=450, null=True, blank=True)
    AMH = models.TextField(max_length=450, null=True, blank=True)
    Testosterone = models.TextField(max_length=450, null=True, blank=True)
    total_T4 = models.TextField(max_length=450, null=True, blank=True)
    total_t3 = models.TextField(max_length=450, null=True, blank=True)
    TSH = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="reprolab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientrepro")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labrepro', on_delete=models.CASCADE)


class Autoimmunity_and_cancer_Test(models.Model):
    investigation_request = models.ManyToManyField(Investigations, related_name="aactest")
    ANA = models.TextField(max_length=450, null=True, blank=True)
    CA_125 = models.TextField(max_length=450, null=True, blank=True)
    CA15_3 = models.TextField(max_length=450, null=True, blank=True)
    CA19_9 = models.TextField(max_length=450, null=True, blank=True)
    CEA = models.TextField(max_length=450, null=True, blank=True)
    PSA = models.TextField(max_length=450, null=True, blank=True)
    confirmed_diagnosis = models.TextField(max_length=450, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(Users, related_name="aaclab", on_delete=models.DO_NOTHING, null=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE, related_name="patientaac")
    lab_owner = models.ForeignKey(Lab, null=True, related_name='labaac', on_delete=models.CASCADE)

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
    shift_sold = models.ForeignKey(Shifts, null=True, related_name='shiftsold', on_delete=models.DO_NOTHING)

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


class CustomerSales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)
    due_date = models.DateField(auto_created=False, null=True, blank=True)
    terms_conditions = models.TextField(max_length=1000, null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='branchforcustomersales', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='customersalesuser', on_delete=models.DO_NOTHING, null=True, default="wriberpos@gmail.com")
    shift_sold = models.ForeignKey(Shifts, null=True, related_name='customershiftsold', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, null=True, related_name='customershiftselling', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.code

    def sold_by(self):
        return self.user.email

    def branch(self):
        return self.branch_owner

    def code_again(self):
        return self.code


class CustomerSalesItems(models.Model):
    sale_id = models.ForeignKey(CustomerSales,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now, null=True)
    branch_owner = models.ForeignKey(Branch, null=True, related_name='forcustomersaleitembranch', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='customersaleitemuser', on_delete=models.DO_NOTHING, null=True)
    shift_sold = models.ForeignKey(Shifts, null=True, related_name='customershiftitemsold', on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, null=True, related_name='customershiftsellingitem', on_delete=models.DO_NOTHING)