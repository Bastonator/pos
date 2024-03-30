# Generated by Django 4.1 on 2024-03-30 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0011_investigations_lab_patient_reproduction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ascetic_fluid_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='autoimmunity_and_cancer_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='cardiac_markers',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='diabetic_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='elements_conc_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='inflammtory_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='ironprofile_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='lipidprofile_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='liver_function_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='pancreatic_enzymes_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='renal_function_test',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.AddField(
            model_name='reproduction',
            name='confirmed_diagnosis',
            field=models.TextField(blank=True, max_length=450, null=True),
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drug', models.TextField(blank=True, null=True)),
                ('dosage', models.TextField(blank=True, null=True)),
                ('is_taking', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='prescription', to=settings.AUTH_USER_MODEL)),
                ('lab_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='labprescription', to='posApp.lab')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patientprescription', to='posApp.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint1', models.TextField(blank=True, null=True)),
                ('complaint2', models.TextField(blank=True, null=True)),
                ('complaint3', models.TextField(blank=True, null=True)),
                ('complaint4', models.TextField(blank=True, null=True)),
                ('query_diagnosis', models.TextField(blank=True, max_length=4500, null=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='complaint', to=settings.AUTH_USER_MODEL)),
                ('lab_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='labcomplaint', to='posApp.lab')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patientcomplaint', to='posApp.patient')),
            ],
        ),
    ]
