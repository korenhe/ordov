from django.shortcuts import render
from django.views import generic

from candidates.models import Candidate
from interviews.models import Interview

# Create your views here.
def index(request):
    context = {}
    return render(request, 'recruit_manager/index.html', context)

class CandidateTable(generic.ListView):
    context_object_name = 't_candidate_list'
    template_name = 'recruit_manager/table_candidates.html'
    def get_queryset(self):
        return Candidate.objects.all().prefetch_related('interview_set')


class InterviewTable(generic.ListView):
    context_object_name = 't_interview_list'
    template_name = 'recruit_manager/table_interviews.html'

    def get_queryset(self):
        return Interview.objects.all()[:5]
