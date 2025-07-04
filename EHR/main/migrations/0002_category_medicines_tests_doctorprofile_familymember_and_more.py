# Generated by Django 5.2.1 on 2025-06-06 07:08

import django.db.models.deletion
import main.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Dentist', 'Dentist'), ('Pediatrician', 'Pediatrician'), ('Neurologist', 'Neurologist'), ('Dermatologist', 'Dermatologist'), ('General', 'General Physician')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='medicines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration_left', models.DateTimeField(auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('dosage', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='tests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('scheduled_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('degree', models.CharField(max_length=255)),
                ('dob', models.DateTimeField(null=True, verbose_name='Date of Birth')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('phone_number', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=120)),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('phone_number', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='family_members', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='family_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_file', models.FileField(upload_to=main.models.upload_to_unique, validators=[main.models.validate_file_size])),
                ('prescription_file', models.FileField(upload_to=main.models.upload_to_unique, validators=[main.models.validate_file_size])),
                ('medicines_name', models.TextField(help_text='Comma-separated medicine names and dosages')),
                ('prescribed_tests', models.TextField(help_text='comma separated test  names')),
                ('uploaded_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
                ('dob', models.DateField(verbose_name='Date of Birth')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('phone_number', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reports', models.FileField(blank=True, null=True, upload_to=main.models.upload_to_unique, validators=[main.models.validate_file_size])),
                ('prescription_file', models.FileField(blank=True, null=True, upload_to=main.models.upload_to_unique, validators=[main.models.validate_file_size])),
                ('scheduled_on', models.DateTimeField()),
                ('venue', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0, verbose_name=((0, 'Pending'), (1, 'Accepted'), (2, 'Rejected')))),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.category')),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.doctorprofile')),
                ('prescribed_medicines', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.medicines')),
                ('prescribed_tests', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.tests')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.userprofile')),
            ],
        ),
        migrations.DeleteModel(
            name='UserSession',
        ),
    ]
