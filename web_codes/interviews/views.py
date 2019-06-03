# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status as rest_status

from .models import Interview, query_interviews_by_args, STATUS_CHOICES

from .serializers import InterviewSerializer

from .models import InterviewSub_Interview, InterviewSub_Interview_Pass
from .serializers import InterviewSub_InterviewSerializer, InterviewSub_Interview_PassSerializer

from .models import InterviewSub_Offer, InterviewSub_Offer_Agree
from .serializers import InterviewSub_OfferSerializer, InterviewSub_Offer_AgreeSerializer

from companies.models import Post
from resumes.models import Resume
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your views here.
class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all().order_by('id')
    serializer_class = InterviewSerializer

    def create(self, request, **kwargs):
        # Update the interview stat here
        is_active = request.data['is_active']
        status = request.data['status']
        postid = request.data['resume']
        resumeid = request.data['post']
        # -1 and -2 has special usage in our system
        # -1 means increating automically
        # -2 means stop

        interviewTarget = None
        if status == -1 or status == -2:
            try:
                interviewTarget = Interview.objects.get(post=postid, resume=resumeid)
            except (ObjectDoesNotExist):
                pass
        if interviewTarget == None and status == -2:
            status = 0
        elif interviewTarget == None and status == -1:
            status = 2
        elif status == -1: # increase automically
            curStat = interviewTarget.status
            status = curStat + 1
        elif status == -2: # stop
            status = interviewTarget.status

        iMap = request.data
        iMap['status'] = status
        interviewSerializer = InterviewSerializer(data=iMap)
        if interviewSerializer.is_valid(raise_exception=True):
            interviewSaved = interviewSerializer.save()
        else:
            pass
        # we should update the
        return Response({}, status=rest_status.HTTP_200_OK, template_name=None, content_type=None)

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

class InterviewSub_InterviewViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Interview.objects.all()
    serializer_class = InterviewSub_InterviewSerializer

class InterviewSub_Interview_PassViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Interview_Pass.objects.all()
    serializer_class = InterviewSub_Interview_PassSerializer

class InterviewSub_OfferViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Offer.objects.all()
    serializer_class = InterviewSub_OfferSerializer

class InterviewSub_Offer_AgreeViewSet(viewsets.ModelViewSet):
    queryset = InterviewSub_Offer_Agree.objects.all()
    serializer_class = InterviewSub_Offer_AgreeSerializer
