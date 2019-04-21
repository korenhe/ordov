from django.shortcuts import render
from django.views import generic

from candidates.models import Candidate

# Create your views here.
def index(request):
    context = {}
    return render(request, 'recruit_manager/index.html', context)

class CandidateTable(generic.ListView):
    context_object_name = 't_candidate_list'
    template_name = 'recruit_manager/tables.html'
    def get_queryset(self):
        return Candidate.objects.all()[:5]
