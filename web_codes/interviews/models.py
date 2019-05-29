# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from candidates.models import Candidate
from companies.models import Post
from resumes.models import Resume
from model_utils import Choices

# Create your models here.

STATUS_CHOICES = (
    (0, '筛选'),
    (1, 'AI面试中'),
    (2, '邀约'),
    (3, '面试'),
    (4, 'OFFER'),
    (5, '入职'),
    (6, '考察'),
    (7, '回款'),
    (8, '完成'),
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
# 面试有许多过程，每个过程分成三种状态, pending, pass, over

class Interview(models.Model):
    class Meta:
        unique_together = (('post', 'resume'), )

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)

    is_active = models.BooleanField(default=1)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    result = models.CharField(max_length=50)

    # manually check
    is_match = models.BooleanField(default=1)

    def __str__(self):
        return '<interview C: %s B: %s' % (self.resume.resume_id, self.post.name)

ORDER_COLUMN_CHOICES = Choices(
    ('0', 'id'),
    ('1', 'resume'),
    ('2', 'resume'),
    ('3', 'post'),
    ('4', 'is_active'),
    ('5', 'status'),
    ('6', 'status'),
)

def query_interviews_by_args(**kwargs):
    draw = int(kwargs.get('draw', [0])[0])
    length = int(kwargs.get('length', [10])[0])
    start = int(kwargs.get('start', [0])[0])
    search_value = kwargs.get('search[value]', [0])[0]
    order_column = kwargs.get('order[0][column]', [0])[0]
    order = kwargs.get('order[0][dir]', [0])[0]

    order_column = ORDER_COLUMN_CHOICES[int(order_column)][1]
    if order == 'desc':
        order_column = '-' + order_column

    queryset = Interview.objects.all()
    total = queryset.count()

    # filter and orderby

    if search_value:
        queryset = queryset.filter(models.Q(post__name__icontains=search_value) |
                                   models.Q(post__department__name__icontains=search_value) |
                                   models.Q(post__department__company__name__icontains=search_value) |
                                   models.Q(resume__username__icontains=search_value))

    # ------
    count = queryset.count()

    queryset = queryset.order_by(order_column)[start:start + length]

    # final decoration

    return {
        'items': queryset,
        'count': count,
        'total': total,
        'draw' : draw,
    }

class Interview_Invite_Agree(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.DateTimeField(auto_now_add=True, auto_now=False)
    contact = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    certification = models.CharField(max_length=500, blank=True, null=True)
    attention = models.CharField(max_length=500, blank=True, null=True)
    other = models.CharField(max_length=500, blank=True, null=True)

class Interview_Invite_Disagree(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)

    address = models.CharField(max_length=50, blank=True, null=True)
    industry = models.CharField(max_length=50, blank=True, null=True)
    salary = models.CharField(max_length=50, blank=True, null=True)
    insurance = models.CharField(max_length=50, blank=True, null=True)
    other = models.CharField(max_length=500, blank=True, null=True)

class OnDuty(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    is_active = models.BooleanField(default = 0)
    status = models.IntegerField(choices=STATUS_ONDUTY_CHOICES, default=0)
    last_modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    result = models.CharField(max_length=50)

    def __str__(self):
        return '<onduty C: %s B: %s' % (self.candidate.user.username, self.post.name)
