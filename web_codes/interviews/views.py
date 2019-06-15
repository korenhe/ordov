# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status as rest_status

from .models import Interview, query_interviews_by_args, STATUS_CHOICES

from .serializers import InterviewSerializer

from .models import InterviewSub_Appointment, InterviewSub_Appointment_Agree
from .serializers import InterviewSub_AppointmentSerializer, InterviewSub_Appointment_AgreeSerializer

from .models import InterviewSub_Interview, InterviewSub_Interview_Pass
from .serializers import InterviewSub_InterviewSerializer, InterviewSub_Interview_PassSerializer

from .models import InterviewSub_Offer, InterviewSub_Offer_Agree
from .serializers import InterviewSub_OfferSerializer, InterviewSub_Offer_AgreeSerializer

from .models import InterviewSub_Probation, InterviewSub_Probation_Fail
from .serializers import InterviewSub_ProbationSerializer, InterviewSub_Probation_FailSerializer

from .models import InterviewSub_Payback, InterviewSub_Payback_Finish
from .serializers import InterviewSub_PaybackSerializer, InterviewSub_Payback_FinishSerializer

from .models import InterviewSub_Terminate
from .serializers import InterviewSub_TerminateSerializer

from companies.models import Post
from resumes.models import Resume

# Create your views here.
class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all().order_by('id')
    serializer_class = InterviewSerializer

    def list(self, request, **kwargs):
        interview = query_interviews_by_args(**request.query_params)

        serializer = InterviewSerializer(interview['items'], many=True)
        result = dict()

        result['data'] = serializer.data
        tds = result['data']

        # here we can modify the response data, and we can add pesudo fields in
        # serializer, as we handled candidate_id
        for td in tds:
            resume_obj = Resume.objects.get(pk=td['resume'])
            resume = resume_obj.username + '(ID=' + str(td['resume']) + ')'

            post_obj = Post.objects.get(pk=td['post'])
            post = '-'.join([post_obj.company.name, post_obj.department.name, post_obj.name])

            td.update({'resume_pk': resume_obj.id})
            td.update({'resume': resume})
            td.update({'post': post})
            td.update({'status_name': STATUS_CHOICES[td['status']][1]})

            if resume_obj.candidate:
                td.update({'linked_candidate': resume_obj.candidate.id})
            else:
                td.update({'linked_candidate': None})
            td.update({'DT_RowId': td['resume']})

        result['draw'] = interview['draw']
        result['recordsTotal'] = int(interview['total'])
        result['recordsFiltered'] = int(interview['count'])

        return Response(result, status=rest_status.HTTP_200_OK, template_name=None, content_type=None)

class InterviewTable(generic.ListView):
    context_object_name = 't_interview_list'
    template_name = 'interviews/table_interviews.html'

    def get_queryset(self):
        return Interview.objects.all()

    def get_context_data(self, **kwargs):
        context = super(InterviewTable, self).get_context_data(**kwargs)
        context['template_table_name'] = 'Interview'
        return context

def Task(request):
    if request.method == 'GET':
        task_array = []
        task_array.append(u"深圳富士通")
        task_array.append(u"北京创图")
        task_array.append(u"上海任宁")
        data = {
           "ai_taskId": task_array
        }
        return JsonResponse(data)

# Interview Appointment SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------
class InterviewSub_AppointmentViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Appointment.objects.all()
    serializer_class = InterviewSub_AppointmentSerializer

class InterviewSub_Appointment_AgreeViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Appointment_Agree.objects.all()
    serializer_class = InterviewSub_Appointment_AgreeSerializer

# Interview Result SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------
class InterviewSub_InterviewViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Interview.objects.all()
    serializer_class = InterviewSub_InterviewSerializer

class InterviewSub_Interview_PassViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Interview_Pass.objects.all()
    serializer_class = InterviewSub_Interview_PassSerializer

# Interview Offer SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------
class InterviewSub_OfferViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Offer.objects.all()
    serializer_class = InterviewSub_OfferSerializer

class InterviewSub_Offer_AgreeViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Offer_Agree.objects.all()
    serializer_class = InterviewSub_Offer_AgreeSerializer

# Interview Probation SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------
class InterviewSub_ProbationViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Probation.objects.all()
    serializer_class = InterviewSub_ProbationSerializer

class InterviewSub_Probation_FailViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Probation_Fail.objects.all()
    serializer_class = InterviewSub_Probation_FailSerializer

# Interview Payback SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------
class InterviewSub_PaybackViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Payback.objects.all()
    serializer_class = InterviewSub_PaybackSerializer

class InterviewSub_Payback_FinishViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Payback_Finish.objects.all()
    serializer_class = InterviewSub_Payback_FinishSerializer

# Interview Terminate SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------
class InterviewSub_TerminateViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Terminate.objects.all()
    serializer_class = InterviewSub_TerminateSerializer

def interviewsub_get_offer_detail(request, interview_id):
    interview_obj = Interview.objects.get(pk=interview_id)
    offers = interview_obj.interviewsub_offer_set.all().order_by('-id')
    #get first, descend, can be multi since updated

    data = {}
    if offers:
        offer_obj = offers[0]
        offer_agrees = offer_obj.interviewsub_offer_agree_set.all()
        assert(len(offer_agrees) == 1)
        #get first and assert one
        if offer_agrees:
            offer_agree_obj = offer_agrees[0]

            #serialize and pass back as json
            offer_agree_serializer = InterviewSub_Offer_AgreeSerializer(offer_agree_obj)
            data = offer_agree_serializer.data
            data.pop('offer_sub')
            return JsonResponse(data)

    return JsonResponse(data)
