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
    
    branch = models.ForeignKey(InstituteBranch,on_delete=models.CASCADE,related_name='fees_branch')
    fees_type = models.CharField(max_length=6, choices=FEES_CHOICES, default='admission')
    amount = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

class Userone(AbstractUser):

    class Meta:
        unique_together = ("enrollment", "branch")
         
    
    # user = models.OnTeoOneField(User, on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex],max_length=17)
    # email = models.EmailField(max_length=70,blank=True)
    enrollment = models.CharField(max_length=30)
    branch = models.ForeignKey(InstituteBranch,on_delete=models.CASCADE,related_name='student_branch',null=True)
    
    COURSE_CHOICES = ((
    ('be','B-TECH'),
    ('mba', 'MBA'),
    ('pharmacy','PHARMACY'),
    ))
    
    course = models.CharField(max_length=6, choices=COURSE_CHOICES, default='be')
    dob = models.DateField(max_length=8,default=datetime.now())
    
    GENDER_CHOICES = ((
    ('male','MALE'),
    ('female', 'FEMALE'),
    ))
    
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')

    address = models.CharField(max_length=15)

    # is_active = models.BooleanField(default=True)