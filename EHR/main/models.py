from django.db import models
from django.contrib.auth.models import User
import  uuid
from  django.core.exceptions  import  ValidationError
from django.conf import settings
import os
from django.utils import timezone
from datetime import timedelta

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=150)  # copy from User
    email = models.EmailField()                  # copy from User
    password = models.CharField(max_length=128)  # store hashed password from User
    dob = models.DateField(verbose_name='Date of Birth')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class  FamilyMember(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    # each family member is pointing back to the parent user who created them
    parent_user =  models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='family_members')
    # making each family member a unique user 
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='family_profile')

    username=models.CharField(max_length=100)
    email=models.EmailField()
    password = models.CharField(max_length=120)

    dob= models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1 , choices=UserProfile.GENDER_CHOICES)
    phone_number =  models.CharField(max_length=15)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} is the family member of {self.parent_user.username}"

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('Cardiologist', 'Cardiologist'),
        ('Dentist', 'Dentist'),
        ('Pediatrician', 'Pediatrician'),
        ('Neurologist', 'Neurologist'),
        ('Dermatologist', 'Dermatologist'),
        ('General', 'General Physician'),
    ]
    category_name  =  models.CharField(max_length=255,choices=CATEGORY_CHOICES)


class DoctorProfile(models.Model):
    user =  models.OneToOneField(User,on_delete=models.CASCADE,related_name='doctor_profile')
    username =  models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=255)
    category_id =  models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    degree =  models.CharField(max_length=255)
    dob=models.DateTimeField(verbose_name='Date of Birth',null=True)
    gender =  models.CharField(max_length=1,choices=UserProfile.GENDER_CHOICES)
    phone_number=models.CharField(max_length=15)
    created_at=  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.category_id.category_name})"

class tests(models.Model):
    name = models.CharField(max_length=255)
    scheduled_on = models.DateTimeField(auto_now_add=True)
  
class medicines(models.Model):
    name = models.CharField(max_length=255)
    dosage = models.IntegerField(default=0)
    duration_left = models.DateTimeField(auto_created=True)
    quantity = models.IntegerField(default=0)


def  validate_file_size(file):
    max_size =  settings.MAX_UPLOAD_SIZE
    if file.size >  max_size:
        raise ValidationError(f"File size should not exceed {max_size // (1024 * 1024)} MB.")

def upload_to_unique(instance,filename):
    ext =  filename.split('.')[-1]
    unique_name  =  f"{uuid.uuid4}.{ext}"
    return  os.path.join('uploads/',unique_name)


class Appointments(models.Model):
    reports = models.FileField(upload_to=upload_to_unique , blank=True   ,null=True,  validators=[validate_file_size])
    prescription_file = models.FileField(upload_to=upload_to_unique, blank=True   ,null=True,  validators=[validate_file_size])
    prescribed_tests = models.ForeignKey(tests,on_delete=models.SET_NULL,null=True)
    prescribed_medicines = models.ForeignKey(medicines,on_delete=models.SET_NULL,null = True)
    user_id = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING)
    doctor_id = models.ForeignKey(DoctorProfile,on_delete=models.DO_NOTHING)
    category_id = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    scheduled_on = models.DateTimeField()
    venue = models.CharField(max_length=255)
    status_types = (
        (0,"Pending"),
        (1,"Accepted"),
        (2,"Rejected"),
    )
    status = models.IntegerField(status_types,default=0)
        
class  MedicalRecord(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='medical_records')
    report_file =  models.FileField(upload_to=upload_to_unique,validators=[validate_file_size],null=True,blank = True)
    prescription_file =  models.FileField(upload_to=upload_to_unique,validators=[validate_file_size],null=True,blank = True)
    medical_category = models.ForeignKey(Category,on_delete=models.DO_NOTHING,default=6)
    medicines_name =  models.TextField(help_text="Comma-separated medicine names and dosages",null=True,blank=True)
    prescribed_tests =  models.TextField(help_text='comma separated test  names',null=True,blank=True)

    uploaded_on  =  models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}'s record ({self.uploaded_on.date()})"
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_sessions')
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'session_key')

class  EmailOTP(models.Model):
    user =  models.ForeignKey(User,on_delete=models.CASCADE)
    otp =  models.CharField(max_length=6)
    created_at =  models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return  self.created_at >= timezone.now() -  timedelta(minutes=5)
