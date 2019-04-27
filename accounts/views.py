# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from accounts.models import UserProfile

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            #step1: store to table user_auth
            form.save()

            #step2: register the userprofile
            data = form.data
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get('user_type')
            user = authenticate(username=username, password=raw_password)
            userprofile = UserProfile(
                user = user,
                user_type = user_type,
            )
            userprofile.save()

            #step3: login and redirect
            login(request, user)
            return HttpResponseRedirect("/manager")
    elif request.method == 'GET':
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})
   
