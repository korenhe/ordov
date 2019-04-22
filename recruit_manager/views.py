from django.shortcuts import render, get_object_or_404
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

class CandidateDetail(generic.DetailView):
    model = Candidate
    context_object_name = 't_candidate'
    template_name = 'recruit_manager/detail_candidate.html'

class InterviewTable(generic.ListView):
    context_object_name = 't_interview_list'
    template_name = 'recruit_manager/table_interviews.html'

    def get_queryset(self):
        return Interview.objects.all()[:5]

def interview_api(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    context = {
        't_candidate': candidate
    }
    return render(request, 'recruit_manager/interview_api.html', context)
