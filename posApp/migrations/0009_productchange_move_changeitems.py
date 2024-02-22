# Generated by Django 4.1 on 2024-02-22 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0008_shifts_sales_shift_sold'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductChange',
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
                ('branch_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changebranch', to='posApp.branch')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changesuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.FloatField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('branch_from', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='movefrom', to='posApp.branch')),
                ('branch_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movebranch', to='posApp.branch')),
                ('branch_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='moveto', to='posApp.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.products')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movingsuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='changeItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('qty', models.FloatField(default=0)),
                ('total', models.FloatField(default=0)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('branch_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changeitembranch', to='posApp.branch')),
                ('change_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.productchange')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posApp.products')),
            ],
        ),
    ]
