# Generated by Django 4.1 on 2024-05-14 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0019_patient_code_alter_test_performed_price_lab_shifts_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customersales',
            name='amount_paid',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=100, null=True),
        ),
        migrations.AddField(
            model_name='customersales',
            name='is_partially_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customersales',
            name='not_paid',
            field=models.BooleanField(default=False),
        ),
    ]
