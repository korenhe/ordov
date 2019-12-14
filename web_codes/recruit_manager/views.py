from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.db import models

from django.contrib.auth.decorators import login_required

import os
import time

from candidates.models import Candidate
from companies.models import Company, Post
from interviews.models import Interview
from resumes.models import Resume
from .load_excel import load_excel

from accounts.models import UserProfile
from permissions.models import ProjectPermission

# Create your views here.
@login_required
def index(request):
    print("------ recruit_manager", request.user)
    tcc = Company.objects.all().count()
    tac = Resume.objects.all().count()
    tic = Interview.objects.all().count()
    tsc = 0

    context = {
        't_company_count': tcc,
        't_candidate_count': tac,
        't_interview_count': tic,
        't_success_count': tsc,
    }
    return render(request, 'recruit_manager/index.html', context)

def upload(request):
    uploaded_file_url=""
    if request.method == 'POST' and not len(request.FILES) is 0 and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']

        now=int(round(time.time()*1000))
        nowStr= time.strftime('Excel-%Y-%m-%d-%H-%M-%S-',time.localtime(now/1000))
        store_name=nowStr + excel_file.name

        fs = FileSystemStorage()
        filename = fs.save(store_name, excel_file)

        # Main logic: Parse the excel
        PROJECT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

        uploaded_file_url = fs.url(filename)
        load_excel.load_excel(PROJECT_DIR+uploaded_file_url)

    context = {
       'uploaded_file_url': uploaded_file_url
    }
    return render(request, 'recruit_manager/upload.html', context)

class CandidateTable(generic.ListView):
    context_object_name = 't_candidate_list'
    template_name = 'candidates/table_candidates.html'
    paginate_by = 10

    def get_queryset_waitting(self):
        candidate_list = Candidate.objects.all().prefetch_related('resume_set')
        return candidate_list

    def get_context_data(self, **kwargs):
        context = super(CandidateTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Candidate'
        return context

def interview_api(request, resume_id, interview_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    interview = get_object_or_404(Interview, pk=interview_id)

    context = {
        't_resume': resume,
        't_interview' : interview,
    }
    return render(request, 'recruit_manager/interview_api.html', context)

def interview_result(request, interview_id):
    interview = get_object_or_404(Interview, pk=interview_id)

    if interview.status < 6:
        interview.status += 1
        interview.save()
    context = {}

    return HttpResponseRedirect(reverse('app_manager:t_interviews'), context)

def invitation_api(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    context = {
        't_resume': resume
    }
    return render(request, 'recruit_manager/invitation_api.html', context)

def invitation_result(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)

    context = {}

    return HttpResponseRedirect(reverse('app_manager:t_interviews'), context)

def resume_statistic(request, post_id):
    resumes_total = Resume.objects.exclude(interview__status=0, interview__post__id=post_id).count()

    queryset_waitting = Resume.objects.exclude(interview__post__id=post_id)
    post_request = None
    try:
        post_request = Post.objects.get(id=post_id)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        pass

    if post_request:
        post_age_min = post_request.age_min or 0
        post_age_max = post_request.age_max or 100
        post_degree_min = post_request.degree_min or 0
        post_degree_max = post_request.degree_max or 100
        post_gender = post_request.gender or ""
        post_province = post_request.address_province
        post_city = post_request.address_city
        post_district = post_request.address_district
        post_resume_latest_modified = post_request.resume_latest_modified

        queryset_waitting = queryset_waitting.filter(models.Q(degree__gte=post_degree_min) &
                                   models.Q(degree__lte=post_degree_max) &
                                   models.Q(age__gte=post_age_min) &
                                   models.Q(age__lte=post_age_max))
        if post_gender.find(u'男') >= 0:
            queryset_waitting = queryset_waitting.filter(models.Q(gender__contains='m'))
        elif post_gender.find(u'女') >= 0:
            queryset_waitting = queryset_waitting.filter(models.Q(gender__contains='f'))

        # post_province/city/district filter
        if post_province and post_province != "":
            queryset_waitting = queryset_waitting.filter(models.Q(expected_province__icontains=post_province))
        if post_city and post_city != "":
            queryset_waitting = queryset_waitting.filter(models.Q(expected_city__icontains=post_city))
        if post_district and post_district != "":
            queryset_waitting = queryset_waitting.filter(models.Q(expected_district__icontains=post_district))
        if post_resume_latest_modified is not None:
            queryset_waitting = queryset_waitting.filter(models.Q(last_modified__gte=post_resume_latest_modified))

    userProfile = UserProfile.objects.get(user=request.user)
    resumes_waitting = queryset_waitting.count()

    if userProfile.user_type != "Manager":
        permission = ProjectPermission.objects.filter(user=userProfile, post=post_request, stage=0)
        if permission:
            pass
        else:
            resumes_waitting = 0

    # resumes_waitting should exclude the post filter ones

    interviews_status_filters = []

    if userProfile.user_type == "Manager":
        for i in range(1, 9):
            interviews_status_filters.append(Resume.objects.filter(interview__status=i, interview__post__id=post_id, interview__is_active=True).count())
        interviews_status_filters.append(Resume.objects.filter(interview__post__id=post_id, interview__is_active=False).count())
    else:
        for i in range(1, 9):
            try:
                permission = ProjectPermission.objects.filter(user=userProfile, post=post_request, stage=i)
                if permission:
                    print(i, Resume.objects.filter(interview__status=i, interview__post__id=post_id, interview__is_active=True).count())
                    interviews_status_filters.append(Resume.objects.filter(interview__status=i, interview__post__id=post_id, interview__is_active=True).count())
                    continue
            except:
                pass
            print(i, 0)
            interviews_status_filters.append(0)
        interviews_status_filters.append(0)

    data = {
        "resumes_total": resumes_total,
        "resumes_waitting": resumes_waitting,
        "interviews_status_filters": interviews_status_filters,
    }
    return JsonResponse(data)
