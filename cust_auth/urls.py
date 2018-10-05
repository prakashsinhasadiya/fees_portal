# -*- coding: utf-8 -*-
import os

from django.conf.urls import url
from django.contrib.auth.views import logout

from .views import (
	Login, Signup,logoutuser,get_branch
)

urlpatterns = [
    url(r'^$', Login.as_view(), name='login'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^logout/$',logoutuser,name="logout"),
	url(r'^get_branch/$',get_branch,name="get_brnach"),
	]