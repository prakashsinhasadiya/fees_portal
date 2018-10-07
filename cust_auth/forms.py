# -*- coding: utf-8 -*-
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cust_auth.models import InstituteRecord,InstituteBranch
from django import forms
from datetime import datetime



class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=30, required=True, widget=forms.TextInput(attrs={'class': "form-control", 'id': "username", 'placeholder': 'User Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control",'id':'password','placeholder':'Password'}))


class SignupForm(forms.Form):

    first_name = forms.CharField(label="First Name", max_length=30, required=True, widget=forms.TextInput(
 	    attrs={'class': "form-control", 'id': "first_name", 'placeholder': 'First Name'}))
    last_name = forms.CharField(label="Last Name", max_length=30, required=True, widget=forms.TextInput(
 	    attrs={'class': "form-control", 'id': "last_name", 'placeholder': 'Last Name'}))
    username = forms.CharField(label="User Name", max_length=30, required=True, widget=forms.TextInput(
 	    attrs={'class': "form-control", 'id': "User Name", 'placeholder': 'User Name'}))
    address = forms.CharField(label="Address" ,max_length=30, required=True, widget=forms.TextInput(attrs={'class': "form-control address",'id':"address",'placeholder': 'Address'}))
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?,?\s?\d{8,13}', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = forms.CharField(label="Mobile" ,validators=[phone_regex],max_length=17, required=True,
                             widget=forms.TextInput(attrs={'class': "form-control",'id':"mobile",'placeholder': 'Mobile Number'}))
    email = forms.EmailField(label="Email",
        required=True, widget=forms.EmailInput(attrs={'class': "form-control",'id':"email",'placeholder': 'Email'}))
    dob = forms.DateTimeField(label="Date of Birth", initial=datetime.now(),widget=forms.DateInput(attrs={'type':'date','id':"dob",'class': "form-control",'placeholder': 'date of birth'}))
    
    password_regex = RegexValidator(regex=r'^((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{6,20})',message="password must be entered in the format: 'one digit and one uppercase and one lowecase and special character.")
    password_1 = forms.CharField(validators=[password_regex],max_length=20, widget=forms.PasswordInput(attrs={'class': "form-control",'id':'password_1','placeholder':'Password'}))
    password_2 = forms.CharField(validators=[password_regex],max_length=20, widget=forms.PasswordInput(attrs={'class': "form-control",'id':'password_2','placeholder':'Confirm Password'}))
    
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = forms.ChoiceField(label="Gender" ,widget=forms.RadioSelect(attrs={'class': "form-control",'id':"gender",'placeholder': 'gender'}), required=True,choices=gender_choices)
   
    institute = forms.ModelChoiceField(queryset = InstituteRecord.objects.all(),widget=forms.Select(attrs={'class': "form-control",'id':"institute",'placeholder': 'Institute'}  ),required=True)

    branch = forms.ModelChoiceField(queryset = InstituteBranch.objects.all(),widget=forms.Select(attrs={'class': "form-control",'id':"branch",'placeholder': 'Branch'}  ),required=True)

    enrollment = forms.CharField(label="Enrollment", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': "form-control", 'id': "enrollment", 'placeholder': 'Enrollment'}))


    COURSE_CHOICES = ((
    ('be','B-TECH'),
    ('mba', 'MBA'),
    ('pharmacy','PHARMACY'),
    ))
    
    course = forms.ChoiceField(choices=COURSE_CHOICES,widget=forms.Select(attrs={'class': "form-control",'id':"course",'placeholder': 'Course'}), required=True)

class ResetPasswordForm(forms.Form):
    username = forms.CharField(label="User Name or Email", max_length=30, required=True, widget=forms.TextInput(
        attrs={'class': "form-control", 'id': "User Name", 'placeholder': 'User Name'}))