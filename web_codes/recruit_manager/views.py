from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

import os
import time

from candidates.models import Candidate
from companies.models import Company
from interviews.models import Interview
from .load_excel import load_excel

# Create your views here.
def index(request):
    tcc = Company.objects.all().count()
    tac = Candidate.objects.all().count()

    context = {
        't_company_count': tcc,
        't_candidate_count': tac,
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
        print("PORJECT_DIR", PROJECT_DIR)

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

    def get_queryset(self):
        candidate_list = Candidate.objects.all().prefetch_related('resume_set')
        return candidate_list

    def get_context_data(self, **kwargs):
        context = super(CandidateTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Candidate'
        return context

def interview_api(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    context = {
        't_candidate': candidate
    }
    return render(request, 'recruit_manager/interview_api.html', context)

def interview_result(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)

    candidate.interviewed = True
    candidate.save()
    context = {}

    return HttpResponseRedirect(reverse('app_manager:t_candidates'), context)
