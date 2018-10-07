# -*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from cust_auth.forms import LoginForm, SignupForm,ResetPasswordForm
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect
from cust_auth.models import InstituteBranch,StudentProfile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
import json
# Create your views here.

fess_payment_url = settings.FEES_PAYMENT or '/admin'
login_redirect_url = settings.LOGIN_URL or ''

class Login(View):

    def get(self, request):
        """
        Return login template
        """
        if request.user.is_authenticated:
            return redirect(fess_payment_url)
        form = LoginForm()
        return render(request, 'user_registrations/login.html', {'form': form})

    def post(self, request):
        """
        Login user and redirect to Profile
        """
        import pdb; pdb.set_trace()
        form = LoginForm()
        login_form = LoginForm(request.POST)
        if not login_form.is_valid():
            return render(request, 'user_registrations/login.html', {'errors': login_form.errors, 'form': form})
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            error = {'general_error': "user don't match"}
            return render(request, 'user_registrations/login.html', {'errors': error, 'form': form})

        if user.check_password(password):
            login(request, user)
            return redirect(fess_payment_url)
        error = {'general_error': "Passwords don't match"}
        return render(request, 'user_registrations/login.html', {'errors': error, 'form': form})


class Signup(View):

    def get(self, request):
        """
        Return signup template
        """
        if request.user.is_authenticated:
            pass
            # return redirect(login_redirect_url)
        form = SignupForm()
        import pdb; pdb.set_trace()
        return render(request, 'user_registrations/signup.html', {'form': form})
    def post(self, request):
        """
        Signup and redirect to Profile
        """
        studentprofile_form = SignupForm(request.POST)
        if studentprofile_form.is_valid():
            username = studentprofile_form.cleaned_data.get('username')
            try:
                user, created = User.objects.get_or_create(username=username)
                if created:
                    password_1 = studentprofile_form.cleaned_data.get('password_1')
                    email = studentprofile_form.cleaned_data.get('email')
                    first_name = studentprofile_form.cleaned_data.get('first_name')
                    last_name = studentprofile_form.cleaned_data.get('last_name')
                    user.set_password(password_1)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.save()
                    mobile = studentprofile_form.cleaned_data.get('mobile')
                    dob = studentprofile_form.cleaned_data.get('dob')
                    address = studentprofile_form.cleaned_data.get('address')
                    institute = studentprofile_form.cleaned_data.get('institute')
                    branch = studentprofile_form.cleaned_data.get('branch')
                    gender = studentprofile_form.cleaned_data.get('gender')
                    enrollment = studentprofile_form.cleaned_data.get('enrollment')
                    course = studentprofile_form.cleaned_data.get('course')
                    import pdb;pdb.set_trace()
                    student_profile, student_profile_create = StudentProfile.objects.get_or_create(user=user)
                    student_profile.mobile = mobile
                    student_profile.address = address
                    student_profile.dob = dob
                    student_profile.enrollment = enrollment
                    student_profile.course = course
                    student_profile.gender = gender
                    student_profile.institute = institute
                    student_profile.branch = branch
                    student_profile.save()
                    login(request, user)
                    return redirect(login_redirect_url)
                else:
                    error = {'general_error': 'User already registered.'}
                    return render(request, 'user_registrations/signup.html', {'errors': error, 'form': studentprofile_form})
            except Exception:
                error = {'general_error': 'Cannot create user at the moment..'}
                return render(request, 'user_registrations/signup.html', {'errors': error, 'form': studentprofile_form})
        else:
            return render(request, 'user_registrations/signup.html', {'errors': studentprofile_form.errors, 'form': studentprofile_form})

def logoutuser(request):
    logout(request)
    return redirect(login_redirect_url)

@csrf_exempt
def get_branch(request):

    records = []
    institute_id = request.POST.get('institute')
    branches = InstituteBranch.objects.filter(institute_name_id=institute_id)
    for branch in branches.values('id','name'):
        records.append(branch)
    return JsonResponse({'status': 'success', 'response': json.dumps(records)})
    # branches = {'id':data.values('id'),'name':data.values('name')}
    # for branch in branches:



class FeesPayment(View):

    def get(self,request):
        import pdb; pdb.set_trace()

class ResetPassword(View):

    def get(self,request):
        import pdb; pdb.set_trace()
        form = ResetPasswordForm()
        return render(request, 'user_registrations/reset_password.html', {'form': form})

    def  post(self,request):

        reset_password_form = ResetPasswordForm(request.POST)
        if not reset_password_form.is_valid():
            return render(request, 'user_registrations/reset_password.html', {'form': reset_password_form, 'errors': reset_password_form.errors})
        username = reset_password_form.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if not user:
            return render(request, 'user_registrations/reset_password.html', {'form': reset_password_form, 'errors': {'general_error': 'User doesnot exist.'}})
        token_obj = PasswordResetTokens.objects.create(
            user=user[0], token=uuid.uuid4().hex)
        url = ''
        url += request.get_host()
        url += '/set_password'
        url += '?token=' + token_obj.token
        # data = {'token' : token_obj.token}
        message = render_to_string('user_registrations/reset_password_email_template.html', {
            'user': user[0],
            'url': url,
        })
        res = send_mail('Password Reset', message, settings.FROM_EMAIL, [user[0].email])
        return render(request, 'user_registrations/reset_email_sent.html')
