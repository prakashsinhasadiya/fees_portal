# -*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from cust_auth.forms import LoginForm, SignupForm, ResetPasswordForm, ConfirmPasswordForm, FeesPaymentForm
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.urls import reverse
from cust_auth.models import InstituteBranch, InstituteFees, StudentProfile, PasswordResetTokens
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import uuid
from django.http import Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import requests
import paypalrestsdk
from paypalrestsdk import Payment

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
        import pdb
        pdb.set_trace()
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
            return redirect(login_redirect_url)
        form = SignupForm()
        return render(request, 'user_registrations/signup.html', {'form': form})

    def post(self, request):
        """
        Signup and redirect to Profile
        """
        studentprofile_form = SignupForm(request.POST)
        if studentprofile_form.is_valid():
            import pdb
            pdb.set_trace()
            password_1 = studentprofile_form.cleaned_data.get('password_1')
            password_2 = studentprofile_form.cleaned_data.get('password_2')
            if password_1 and password_2 and password_1 != password_2:
                message = "Passwords do not match"
                raise ValidationError(message)
            username = studentprofile_form.cleaned_data.get('username')
            try:
                user, created = User.objects.get_or_create(username=username)
                if created:
                    password_1 = studentprofile_form.cleaned_data.get(
                        'password_1')
                    email = studentprofile_form.cleaned_data.get('email')
                    first_name = studentprofile_form.cleaned_data.get(
                        'first_name')
                    last_name = studentprofile_form.cleaned_data.get(
                        'last_name')
                    user.set_password(password_1)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.save()
                    mobile = studentprofile_form.cleaned_data.get('mobile')
                    dob = studentprofile_form.cleaned_data.get('dob')
                    address = studentprofile_form.cleaned_data.get('address')
                    institute = studentprofile_form.cleaned_data.get(
                        'institute')
                    branch = studentprofile_form.cleaned_data.get('branch')
                    gender = studentprofile_form.cleaned_data.get('gender')
                    enrollment = studentprofile_form.cleaned_data.get(
                        'enrollment')
                    course = studentprofile_form.cleaned_data.get('course')
                    student_profile, student_profile_create = StudentProfile.objects.get_or_create(
                        user=user)
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
    for branch in branches.values('id', 'name'):
        records.append(branch)
    return JsonResponse({'status': 'success', 'response': json.dumps(records)})
    # branches = {'id':data.values('id'),'name':data.values('name')}
    # for branch in branches:


class ResetPassword(View):

    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'user_registrations/reset_password.html', {'form': form})

    def post(self, request):

        reset_password_form = ResetPasswordForm(request.POST)
        import pdb
        pdb.set_trace()
        if not reset_password_form.is_valid():
            return render(request, 'user_registrations/reset_password.html', {'form': reset_password_form, 'errors': reset_password_form.errors})

        def user_send_mail(self, user):

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
            res = send_mail('Password Reset', message, settings.FROM_EMAIL, [
                            user[0].email], fail_silently=False)

        username = reset_password_form.cleaned_data.get('username')
        user_email = User.objects.filter(email=username)
        if not user_email:
            user = User.objects.filter(username=username)
            if not user:
                return render(request, 'user_registrations/reset_password.html', {'form': reset_password_form, 'errors': {'general_error': 'User doesnot exist.'}})
            else:
                user_send_mail(self, user)
                return render(request, 'user_registrations/email_send.html')
        else:
            user_send_mail(self, user_email)
            return render(request, 'user_registrations/email_send.html')


class SetPassword(View):

    def get(self, request):
        """
        Check if authorized to reset password.
        Return reset password template
        """
        form = ConfirmPasswordForm()
        token = request.GET.get('token')
        if not token:
            raise Http404('Page not found.')
        token_obj = PasswordResetTokens.objects.filter(token=token)
        import pdb
        pdb.set_trace()
        if not token_obj:
            raise Http404('Fake token supplied.')
        # tz = pytz.timezone("UTC")
        # if tz.localize(datetime.now(), is_dst=None) > token_obj[0].expired_time:
        #     raise Http404('Token Expired. Try again')
        return render(request, 'user_registrations/set_password.html', {'form': form, 'token': token})

    def post(self, request):
        """
        Save new password and redirect to Login
        """
        import pdb
        pdb.set_trace()
        form = ConfirmPasswordForm(request.POST)
        token = request.GET.get('token')
        if not token:
            raise Http404('Tocken not found.')
        if not form.is_valid():
            import pdb
            pdb.set_trace()
            return render(request, 'user_registrations/set_password.html', {'form': form, 'token': token, 'errors': form.errors})
        token_obj = PasswordResetTokens.objects.filter(token=token)
        if not token_obj:
            raise Http404('Fake token supplied.')
        password_1 = form.cleaned_data.get('password_1')
        user = token_obj[0].user
        user.set_password(password_1)
        user.save()
        token_obj[0].delete()
        return HttpResponseRedirect(reverse('login'))


class FeesPayment(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(login_redirect_url)
        form = FeesPaymentForm()
        objects = request.user
        form['institute'].initial = objects.studentprofile.branch.institute_name
        form['branch'].initial = objects.studentprofile.branch
        form['enrollment'].initial = objects.studentprofile.enrollment
        return render(request, 'user_registrations/fees_payment.html', {'form': form, 'object': objects})

    def post(self, request):

        fees_types = InstituteFees.objects.filter(
            fees_type__in=request.POST.getlist('fees_type'))
        fees_list = []
        total_amount = 0
        import pdb
        pdb.set_trace()
        for fees_type in fees_types:
            fees_list_dict = {}
            fees_list_dict['name'] = fees_type.fees_type
            fees_list_dict['price'] = fees_type.amount
            fees_list_dict['currency'] = "USD"
            fees_list_dict["quantity"] = 1
            fees_list.append(fees_list_dict)
            total_amount += fees_type.amount
        total_amount_value = {'total': total_amount, 'currency': 'USD'}

        paypalrestsdk.configure({
            "mode": "sandbox",  # sandbox or live
            "client_id": "AWNIRUxctIc8ELjCrYLK8Zbv9L0EqL0aLplmLHpXPaPT_BVXINg66096i4jIO6i448h2fH-7sdaaiAtE",
            "client_secret": "ECnA0hUuNZShemfJq5sD-UAfDUuEbr1i5j6RQcHdZJZiDkrYMTo1S6kA6E_OEwA_zX8FMEz4-57TfOaN"})

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:8000/payment_return_response",
                "cancel_url": "http://localhost:8000/"},
            "transactions": [{
                "item_list": {"items": fees_list},
                "amount": total_amount_value,
                "description": "This is the payment transaction description."}]})
        if payment.create():
            print("Payment created successfully")

            for link in payment.links:
                if link.rel == "approval_url":
                    # Convert to str to avoid Google App Engine Unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                    approval_url = str(link.href)
                    print("Redirect for approval: %s" % (approval_url))
                    return HttpResponseRedirect(approval_url)
        else:
            import pdb
            pdb.set_trace()
            print(payment.error)
            print(response.text)


@csrf_exempt
def amount_value(request):

    records = {}
    institute_id = request.POST.get('institute')
    branch_name = request.POST.get('branch')
    try:
        for branc_institiute_value in InstituteBranch.objects.filter(name=branch_name).values('id', 'institute_name_id'):
            records.update(branc_institiute_value)
        amount_object = InstituteFees.objects.filter(
            branch_id=branc_institiute_value.get('id'), fees_type=request.POST.get('value'))
        if amount_object:
            for amount_obj in amount_object:
                amount = amount_obj.amount
                result = dict(request.POST)
                if request.POST.get('selected') == 'true':
                    result['amount'] = abs(
                        amount + float(request.POST.get('amount_value')))
                else:
                    result['amount'] = abs(
                        amount - float(request.POST.get('amount_value')))
                return JsonResponse({'status': 'success', 'response': json.dumps(result)})
        else:
            result = dict(request.POST)
            result['error'] = 'this fees type are not exist'
            return JsonResponse({'status': 'fail', 'response': json.dumps(result)})
    except Exception:
        result = dict(request.POST)
        result['error'] = 'somthing wrong'
        return JsonResponse({'status': 'fail', 'response': json.dumps(result)})


class PaymentReturnResponse(View):

    def get(self, request):

        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')

        paypalrestsdk.configure({
            "mode": "sandbox",  # sandbox or live
            "client_id": "AWNIRUxctIc8ELjCrYLK8Zbv9L0EqL0aLplmLHpXPaPT_BVXINg66096i4jIO6i448h2fH-7sdaaiAtE",
            "client_secret": "ECnA0hUuNZShemfJq5sD-UAfDUuEbr1i5j6RQcHdZJZiDkrYMTo1S6kA6E_OEwA_zX8FMEz4-57TfOaN"})
        payment = Payment.find(payment_id)

        import pdb
        pdb.set_trace()
        # if payment.execute({'payer_id':payer_id})
        # form = FeesPaymentForm()
        # objects = request.user
        # form['institute'].initial = objects.studentprofile.branch.institute_name
        # form['branch'].initial = objects.studentprofile.branch
        # form['enrollment'].initial = objects.studentprofile.enrollment
        # return render(request, 'user_registrations/fees_payment.html',
        # {'form': form,'object':objects})
