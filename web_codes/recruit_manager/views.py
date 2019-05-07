from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect

from candidates.models import Candidate
from interviews.models import Interview

# Create your views here.
def index(request):
    tcc = Company.objects.all().count()
    tac = Candidate.objects.all().count()

    context = {
        't_company_count': tcc,
        't_candidate_count': tac,
    }
    return render(request, 'recruit_manager/index.html', context)

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

class InterviewTable(generic.ListView):
    context_object_name = 't_interview_list'
    template_name = 'recruit_manager/table_interviews.html'

    def get_queryset(self):
        return Interview.objects.all()

    def get_context_data(self, **kwargs):
        context = super(InterviewTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Interview'
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
