# Generated by Django 4.1 on 2024-01-30 16:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('location', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('user', models.ManyToManyField(null=True, related_name='branchusers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('status', models.IntegerField(blank=True, default=1, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('branch_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categorybranch', to='posApp.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('price', models.FloatField(default=0)),
                ('status', models.IntegerField(default=1)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('expiry_date', models.DateField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('branch_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productsbranch', to='posApp.branch')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('sub_total', models.FloatField(default=0)),
                ('grand_total', models.FloatField(default=0)),
                ('tax_amount', models.FloatField(default=0)),
                ('tax', models.FloatField(default=0)),
                ('tendered_amount', models.FloatField(default=0)),
                ('amount_change', models.FloatField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('branch_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salesbranch', to='posApp.branch')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salesuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='salesItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('qty', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('branch_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saleitembranch', to='posApp.branch')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.products')),
                ('sale_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.sales')),
            ],
        ),
    ]
