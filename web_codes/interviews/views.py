# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse, HttpResponse
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

from rest_framework import status
from third_party.views import getBaiyingTaskList, importTaskCustomer

import json

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

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def UpdateAIStatus(request):
    if request.method == 'POST':
        print("post------------", request.POST)
        post_id_S = request.POST['post_id']
        subStatus = request.POST['ai_status']
        subStatusAction = request.POST['ai_status_action']
        if post_id_S == '' or subStatus == '' or subStatusAction == '':
            return
        post_id = int(post_id_S)
        if subStatusAction == '通过':
            Interview.objects.filter(post_id=post_id, status=1, sub_status=subStatus).update(status=2, sub_status='邀约')
        elif subStatusAction == '不通过':
            Interview.objects.filter(post_id=post_id, status=1, sub_status=subStatus).update(status=1, is_active=False)
        return HttpResponse("success")

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def Task(request):
    if request.method == 'GET':
        task_array = getBaiyingTaskList()
        data = {
           "ai_taskId": task_array
        }
        return JsonResponse(data)
    elif request.method == 'POST':
        print("post------------", request.POST)
        ai_task = request.POST['config_ai_task_name']
        candidate_name = request.POST['ai_candidate_name']
        candidate_phone = request.POST['ai_candidate_phone']
        if ai_task == "" or candidate_name == "" or candidate_phone == "":
            return
        # This is test
        # replace phone with my phone number
        # split the ai_task_id
        postInfo = Post.objects.get(baiying_task_name=ai_task)
        taskid = postInfo.baiying_task_id

        # Do not set phone during daily test, remove this line oneline
        candidate_phone = '00000000000'
        print("to Import", taskid, candidate_name, candidate_phone)
        importTaskCustomer(15960, taskid, candidate_name, candidate_phone) 
        return HttpResponse("success")
    return HttpResponse("fail")

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

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def aiTest(request):
    if request.method == "POST":
        returnDataStr = request.body

        print(returnDataStr)
        #returnDataStr = getPesudoResponse()
        returnData = json.loads(returnDataStr)

        sceneInfo = returnData.get('data').get('data').get('sceneInstance')
        if sceneInfo is None:
            return HttpResponse("fail")
        print('\n\n\nsceneInfo', sceneInfo)
        companyId = sceneInfo.get('companyId')
        callJobId = sceneInfo.get('callJobId')
        candidate = sceneInfo.get('customerName')
        candidate_phone = sceneInfo.get('customerTelephone')
        status = sceneInfo.get('status')
        finishstatus = sceneInfo.get('finishStatus')

        postInfo = None
        resumeInfo = None
        try:
            postInfo = Post.objects.get(baiying_task_id=callJobId)
            resumeInfo = Resume.objects.get(phone_number=candidate_phone)
        except:
            return HttpResponse("fail")

        if postInfo is None or resumeInfo is None:
            print("Not imported into db now")
            return HttpResponse("fail")

        interviewInfo = Interview.objects.get(resume=resumeInfo, post=postInfo)
        if interviewInfo is None:
            print("No such item in interview")
            return HttpResponse("fail")
        if interviewInfo.status != 1:
            print("Steal Info interview")
            return HttpResponse("fail")

        print("companyId:", companyId, " callJobId:", callJobId, " candiate: ", candidate, "phone: ", candidate_phone)
        if status == 2 and finishstatus == 2:
            #未接通case
            interviewInfo.sub_status = '未接通AI'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 1:
            interviewInfo.sub_status = '拒绝'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 3:
            interviewInfo.sub_status = '主叫号码不可用'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 4:
            interviewInfo.sub_status = '空号'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 5:
            interviewInfo.sub_status = '关机'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 6:
            interviewInfo.sub_status = '占线'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 7:
            interviewInfo.sub_status = '停机'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 8:
            interviewInfo.sub_status = '未接'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 9:
            interviewInfo.sub_status = '主叫欠费'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 10:
            interviewInfo.sub_status = '呼损'
            interviewInfo.save()
            return HttpResponse("fail")
        if status == 2 and finishstatus == 11:
            interviewInfo.sub_status = '黑名单'
            interviewInfo.save()
            return HttpResponse("fail")
        elif status == 2 and finishstatus == 0:
            #已经接通
            taskResultInfo = returnData.get('data').get('data').get('taskResult')
            if taskResultInfo is None:
                return HttpResponse("fail")
            for result in taskResultInfo:
                resultName = result.get('resultName')
                resultValue = result.get('resultValue')
                if resultName.find('客户意向等级') >= 0:
                    interviewInfo.sub_status = resultValue
                    interviewInfo.save()
                    break
        else:
            interviewInfo.sub_status = '未知状态'
            interviewInfo.save()
            return HttpResponse("fail")

    if request.method == "GET":
        print("Get")
    return HttpResponse("success")
