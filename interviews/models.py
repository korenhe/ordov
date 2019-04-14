# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from candidates.models import Candidate
from companies.models import Post

# Create your models here.

STATUS_CHOICES = (
    (0, 'Open'),
    (1, '面试前沟通(AI/人工面试)'),
    (2, '面试1'),
    (3, '面试2'),
    (4, '面试3'),
    (5, '发放offer'),
    (6, 'finish'),
)

STATUS_ONDUTY_CHOICES = (
    (0, 'Open'), 
    (1, '入职确认'), 
    (2, '考察期'),
    (3, 'finish'),
)

# 某公司和某个人对应着关系
# 一次面试按理说的话，也是有很多
# 每一次的面试记录也都要留下来

class Interview(models.Model):
    post = models.ForeignKey(Post)
    candidate = models.ForeignKey(Candidate)
    is_active = models.BooleanField(default=1)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    result = models.CharField(max_length=50)

    def __str__(self):
        return '<interview C: %s B: %s' % (candidate.name, post.name)

class OnDuty(models.Model):
    post = models.ForeignKey(Post)
    candidate = models.ForeignKey(Candidate)
    is_active = models.BooleanField(default = 0)
    status = models.IntegerField(choices=STATUS_ONDUTY_CHOICES, default=0)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    result = models.CharField(max_length=50)

    def __str__(self):
        return '<onduty C: %s B: %s' % (candidate.name, post.name)
    

    
