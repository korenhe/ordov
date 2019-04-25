# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import UserApplyStep1Form, UserApplyStep2Form

from resumes.models import Resume
from accounts.models import UserProfile

from .models import Candidate

# Create your views here.

def apply(request):
    key = request.GET.get('key', None)
    user = UserProfile.verify_token(key)

    if not key and request.method == 'POST':
        form = UserApplyStep1Form(request.POST)
        if form.is_valid():
            data = form.data
            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            phone_num = data['phone']

            user, created = User.objects.get_or_create(
                first_name = first_name,
                last_name = last_name,
                email=email,
                username=email
            )
            if not created:
                messages.add_message(request, messages.ERROR,
                    email + ' has already been registerd.')
            else:
                userprofile = UserProfile(
                    user = user,
                    user_type = 'Candidate'
                )
                userprofile.save()
                key = user.userprofile.generate_token()
                return HttpResponseRedirect(
                    reverse('candidate_apply') + '?key=' + key)
    elif not key and request.method == 'GET':
        print("not key and GET")
        form = UserApplyStep1Form()
    elif key and user and request.method == 'POST':
        form = UserApplyStep2Form(request.POST, request.FILES)
        if form.is_valid():
            files = form.files
            data = form.data
            try:
                candidate = user.candidate
            except Candidate.DoesNotExist:
                candidate = Candidate.objects.create(user=user)

            resume = Resume(
                candidate = candidate,
                resume_id = 1,
                visible = True,
            )
            resume.save()
            messages.add_message(request, messages.SUCCESS,
                'Form submmited successfully.')
            return HttpResponseRedirect(
                    reverse('candidate_apply_success') + '?key=' + key
                    )
    elif key and user and request.method == 'GET':
        form = UserApplyStep2Form()
    else:
        messages.add_message(request, messages.ERROR,
            'A valid application key is required to submit doc' + 'Please contact the administrator.')
        form = None
    return render(request, 'candidates/apply.html', {'form': form})

def apply_success(request):
    key = request.GET.get('key', None)
    user = UserProfile.verify_token(key)

    if not key or not user:
        messages.add_message(request, messages.ERROR,
            'A valid application key is required to view this page.')
    else:
        return HttpResponseRedirect('/manager')
        jobs_url = reverse('jobs') + '?key=' + key
        availablility_url = reverse('available', args=[user.id]) + '?key=' + key
    return render(request, 'candidate/apply.html',
        {'success':'success', 'jobs_url':jobs_url,'availability_url': availability_url})
