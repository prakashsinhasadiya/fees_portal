from django.db import models
from model_utils.models import TimeStampedModel
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime


class InstituteRecord(TimeStampedModel):

    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to='picture')
    email = models.EmailField(max_length=70,blank=True)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex],max_length=17)
    brochure =  models.FileField(upload_to='picture')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class InstituteBranch(TimeStampedModel):

    institute_name = models.ForeignKey(InstituteRecord, on_delete=models.CASCADE, related_name='branch_institute')
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True, null=True)
    logo = models.ImageField(upload_to='picture')
    email = models.EmailField(max_length=70,blank=True)
    address = models.CharField(max_length=70)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex],max_length=17)
    brochure =  models.FileField(upload_to='picture')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class InstituteFees(TimeStampedModel):

    FEES_CHOICES = (
    ('admission','ADMISSION'),
    ('exam', 'EXAM'),
    ('hostel','HOSTEL'),
    ('transportation','TRANSPORTATION'),
    )
    class Meta:
        unique_together = ("fees_type", "branch")
    
    branch = models.ForeignKey(InstituteBranch,on_delete=models.CASCADE,related_name='fees_branch')
    fees_type = models.CharField(max_length=20, choices=FEES_CHOICES, default='admission')
    amount = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class StudentProfile(TimeStampedModel):

    class Meta:
        unique_together = ("enrollment", "branch")
         
    

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex],max_length=17)
    enrollment = models.CharField(max_length=30)
    branch = models.ForeignKey(InstituteBranch,on_delete=models.CASCADE,related_name='student_branch',null=True)
    
    COURSE_CHOICES = ((
    ('be','B-TECH'),
    ('mba', 'MBA'),
    ('pharmacy','PHARMACY'),
    ))
    
    course = models.CharField(max_length=8, choices=COURSE_CHOICES, default='be')
    dob = models.DateField(null=True)
    
    GENDER_CHOICES = ((
    ('male','MALE'),
    ('female', 'FEMALE'),
    ))
    
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')

    address = models.CharField(max_length=15)

    # is_active = models.BooleanField(default=True)


class PasswordResetTokens(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_token')
    token = models.CharField("Tocken ID", max_length=60, null=False, blank=False)

# class FeesTransactionDetails(TimeStampedModel):

#     student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_transacction')
#     amount =  models.FloatField()
#     transaction_dump = models.CharField()
#     