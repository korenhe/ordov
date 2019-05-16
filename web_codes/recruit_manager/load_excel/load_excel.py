#-*- coding=utf-8 -*-
import os
import xlrd, xlwt
import json
from .resume_template import iPos
from .resume_basic_info  import create_or_update_basic_info
from .resume_education_info import update_education_info
from .resume_experience_info import update_experience_info
from .resume_certification_info import update_language_info, update_certification_info

def test_load_excel():
    filename="/code/recruit_manager/static/resume_template_2003.xls"
    load_excel(filename)

def load_excel(filename):
    data = xlrd.open_workbook(filename, formatting_info=True)
    table = data.sheets()[0]
    headerList = map(lambda x:x.value, table.row(1))
    headerSet = set(headerList)

    # Found the basic info and update the pos
    if u'简历渠道' in headerSet and u'电话号码' in headerSet:
        FoundBLine=True
    else:
        print("This is not a valid Excel")
        return

    print("Begin to Parsing...")
    #for i, value in enumerate(table.row(1)):
    #        iPos[value] = i
    # Found the comment info line

    # Iterate each row to get the resume items
    # Attention, how to check the combined cells

    curValidPhone = ""
    validItem = True
    for rownum in range(2, table.nrows):
        curRowList = list(map(lambda x:x.value, table.row(rownum)))
        phone = curRowList[iPos['PHONE']].strip()
        if not phone == "":
            curValidPhone = phone
            # firstly, the basic resume info should be updated
            if not create_or_update_basic_info(curRowList, curValidPhone):
                validItem = False
                continue
            else:
                validItem = True
            # education/experience/certification info should be updated basing on phone
            update_education_info(curRowList, curValidPhone)
            update_experience_info(curRowList, curValidPhone)
            update_language_info(curRowList, curValidPhone)
            update_certification_info(curRowList, curValidPhone)
        elif validItem == True:
            pass
            # education/experience/certification info should be updated basing on phone
            update_education_info(curRowList, curValidPhone)
            update_experience_info(curRowList, curValidPhone)
            update_language_info(curRowList, curValidPhone)
            update_certification_info(curRowList, curValidPhone)

        #for colnum in xrange(table.ncols):
if __name__ == "__main__":
    read_excel()

