from rest_framework import serializers

from .models import Interview
from .models import Offer, InterviewLogCommon
from .models import InterviewSub_Interview, InterviewSub_Interview_Pass

class InterviewSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    def get_id(self, interview):
        return interview.id

    class Meta:
        model = Interview
        fields = (
            'id',
            'resume',
            'post',
            'is_active',
            'status',
            'result',
        )

class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            'resume',
            'post',
            'interview',
            'salary',
            'entry_date',
            'baoxian',
            'linkman',
            'linkman_phone',
            'beizhu',
        )

class InterviewLogCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewLogCommon
        fields = (
            'interview',
            'status',
            'passInter',
            'result',
        )

class InterviewSub_InterviewSerializer(serializers.ModelSerializer):
    # pass in result(either PASS or NOTGO), then serialize and generate to object
    # then use the generated id, construct Interview result
    class Meta:
        model = InterviewSub_Interview
        fields = (
            'interview',
            'result_type',
        )

class InterviewSub_Interview_PassSerializer(serializers.ModelSerializer):
    interviewsub = InterviewSub_InterviewSerializer(required=True)
    class Meta:
        model = InterviewSub_Interview_Pass
        fields = (
            'interviewsub',
            'reason',
            'description',
            'comments',
            'notes',
        )

    def create(self, validated_data):
        interviewsub_data = validated_data.pop('interviewsub')

        interviewsub_ = InterviewSub_InterviewSerializer.create(InterviewSub_InterviewSerializer(), validated_data=interviewsub_data)

        interviewsub_pass, created = InterviewSub_Interview_Pass.objects.update_or_create(
            interviewsub=interviewsub_,
            **validated_data)

        # update interview table
        interview = Interview.objects.get(pk=interviewsub_.interview.id)
        interview.status = 4
        interview.save()

        return interviewsub_pass
