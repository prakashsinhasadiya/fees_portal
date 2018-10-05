# -*- coding: utf-8 -*-

from django.views import View
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render
from cust_auth.forms import LoginForm, SignupForm
from django.views.decorators.csrf import csrf_protect

# Create your views here.


class Login(View):

    def get(self, request):
        """
        Return login template
        """
        if request.user.is_authenticated:
            pass

        form = LoginForm()
        return render(request, 'user_registrations/login.html', {'form': form})
        import pdb; pdb.set_trace()

    def post(self, request):
        """
        Login user and redirect to Profile
        """
        import pdb; pdb.set_trace()


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
        import pdb; pdb.set_trace()


def logoutuser(request):
    logout(request)
    return redirect(login_redirect_url)

@csrf_protect
def get_branch(request):
    import pdb; pdb.set_trace()