from django.shortcuts import render
import json

# Create your views here.
from .baiying import api as baiying

def getBaiyingTaskList():

    # Step1: to get the company id
    company_list_str = baiying.get_companys()
    company_json = json.loads(company_list_str)
    company_list = company_json.get('data')
    #print("company_list", company_list_str.decode(encoding='utf-8'))
    if company_list is None:
        return None
    company_id = company_list[0].get('companyId')
    print("company_id: ", company_id)

    # Step2: to get the task list
    task_list_str = baiying.getCompanyTaskList(company_id)
    task_json = json.loads(task_list_str)
    if task_json.get('data') is None or task_json.get('data').get('list') is None:
        return None
    task_list = task_json.get('data').get('list')
    taskList = []
    for task in task_list:
        item = [task.get('jobName') +"-"+ str(task.get('callJobId')), task.get('jobName')]
        taskList.append(item)
    return taskList
    
    # Step3: 

def importTaskCustomer(companyId, taskId, username, phone_number):
    baiying.importTaskCustomer(companyId, taskId, username, phone_number)

