# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from resumes.models import Resume
# Create your models here.

#
# TODO: 工作经历表关联company表
# 与 Employee 表是一对多的关系，即一个应聘者包含多个
# 让员工去填公司全称简直是噩梦
class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, default='')
    start = models.DateField()
    end = models.DateField()

    # company info
    company_name = models.CharField(max_length=50)
    department_name = models.CharField(max_length=50)
    post_name = models.CharField(max_length=50)
                # TODO: merge province/city/
    work_province = models.CharField(max_length=20)
    work_city = models.CharField(max_length=30)
    work_district = models.CharField(max_length=30)

    #
    level = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    salary = models.IntegerField(default=0)
    leave_reason = models.CharField(max_length=20)
    zuoxi = models.CharField(max_length=20)

    witness = models.CharField(max_length=20)
    witness_phone = PhoneNumberField(null=True, blank=False)

    def __str__(self):
        return '%s at %s' % (self.candidate.user.username, self.company_name)

