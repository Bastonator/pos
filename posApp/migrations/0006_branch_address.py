# Generated by Django 4.1 on 2024-01-31 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0005_products_cost_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='address',
            field=models.CharField(blank=True, max_length=555, null=True),
        ),
    ]