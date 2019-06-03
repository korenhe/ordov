from rest_framework import serializers

from .models import Interview
from .models import InterviewLogCommon
from .models import InterviewSub_Interview, InterviewSub_Interview_Pass
from .models import InterviewSub_Offer, InterviewSub_Offer_Agree

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

class InterviewSub_OfferSerializer(serializers.ModelSerializer):
    # pass in result(either PASS or NOTGO), then serialize and generate to object
    # then use the generated id, construct Interview result
    class Meta:
        model = InterviewSub_Offer
        fields = (
            'interview',
            'result_type',
        )

class InterviewSub_Offer_AgreeSerializer(serializers.ModelSerializer):
    offersub = InterviewSub_OfferSerializer(required=True)
    class Meta:
        model = InterviewSub_Offer_Agree
        fields = (
            'offersub',
            'date',
            'contact',
            'contact_phone',
            'address',
            'postname',
            'certification',
            'salary',
            'notes',
        )

    def create(self, validated_data):
        offersub_data = validated_data.pop('offersub')

        offersub_ = InterviewSub_OfferSerializer.create(InterviewSub_OfferSerializer(), validated_data=offersub_data)

        offersub_agree, created = InterviewSub_Offer_Agree.objects.update_or_create(
            offersub=offersub_,
            **validated_data)

        # update interview table
        interview = Interview.objects.get(pk=offersub_.interview.id)
        interview.status = 5
        interview.save()

        return offersub_
