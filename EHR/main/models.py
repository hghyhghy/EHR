from django.db import models
from django.contrib.auth.models import User

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
    # each family member is pointing back to the parent user who created them
    parent_user =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='faamily_members')
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
class Appointments(models.Model):
    reports = models.CharField(max_length = 255)
    prescription_file = models.CharField(max_length = 255)
    prescribed_tests = models.ForeignKey(tests,on_delete=models.CASCADE,null=True)
    prescribed_medicines = models.ForeignKey(medicines,on_delete=models.CASCADE,null = True)
    user_id = models.ForeignKey(UserProfile,on_delete=models.DO_NOTHING)
    doctor_id = models.ForeignKey(DoctorProfile,on_delete=models.DO_NOTHING)
    catagory_id = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    scheduled_on = models.DateTimeField()
    venue = models.CharField(max_length=255)
        