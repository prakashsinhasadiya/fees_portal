# -*- coding: utf-8 -*-
import os

from django.conf.urls import url
from django.contrib.auth.views import logout

from .views import (
	Login, Signup,logoutuser,get_branch,amount_value,FeesPayment,ResetPassword,SetPassword,PaymentReturnResponse
)

urlpatterns = [
    url(r'^$', Login.as_view(), name='login'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^logout/$',logoutuser,name="logout"),
	url(r'^get_branch/$',get_branch,name="get_brnach"),
	url(r'^fees_payment/$',FeesPayment.as_view(),name="fees_payment"),
	url(r'^reset_password/$',ResetPassword.as_view(),name="reset_password"),
	url(r'^set_password/$', SetPassword.as_view(), name='set_password'),
	url(r'^amount_value/$',amount_value,name="amount_value"),
	url(r'^payment_return_response',PaymentReturnResponse.as_view(),name="payment_return_response"),
	]