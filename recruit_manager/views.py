from django.shortcuts import render, get_object_or_404
from django.views import generic

from candidates.models import Candidate
from interviews.models import Interview
from resumes.models import Resume

# Create your views here.
def index(request):
    context = {}
    return render(request, 'recruit_manager/index.html', context)

class CandidateTable(generic.ListView):
    context_object_name = 't_candidate_list'
    template_name = 'recruit_manager/table_basic.html'

    def get_queryset(self):
        return Candidate.objects.all().prefetch_related('interview_set')

    def get_context_data(self, **kwargs):
        context = super(CandidateTable, self).get_context_data(**kwargs)
        context['template_table_template'] = 'recruit_manager/table_candidates.html'
        context['template_table_name'] = 'Candidate'
        return context

class InterviewTable(generic.ListView):
    context_object_name = 't_interview_list'
    template_name = 'recruit_manager/table_basic.html'

    def get_queryset(self):
        return Interview.objects.all()[:5]

    def get_context_data(self, **kwargs):
        context = super(InterviewTable, self).get_context_data(**kwargs)
        context['template_table_template'] = 'recruit_manager/table_interviews.html'
        context['template_table_name'] = 'Interview'
        return context

def interview_api(request, candidate_id):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    context = {
        't_candidate': candidate
    }
    return render(request, 'recruit_manager/interview_api.html', context)

class ResumeTable(generic.ListView):
    context_object_name = 't_resume_list'
    template_name = 'recruit_manager/table_basic.html'

    def get_queryset(self):
        return Resume.objects.all()[:5]

    def get_context_data(self, **kwargs):
        context = super(ResumeTable, self).get_context_data(**kwargs)
        context['template_table_template'] = 'recruit_manager/table_resumes.html'
        context['template_table_name'] = 'Resume'
        return context

class ResumeDetail(generic.DetailView):
    model = Resume
    context_object_name = 't_resume_detail'
    template_name = 'recruit_manager/detail_resume.html'
