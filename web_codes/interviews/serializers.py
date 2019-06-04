from rest_framework import serializers

from .models import Interview
from .models import InterviewLogCommon

from .models import InterviewSub_Appointment, InterviewSub_Appointment_Agree
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

# Interview Appointment SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------
class InterviewSub_AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSub_Appointment
        fields = (
            'interview',
            'result_type',
        )

class InterviewSub_Appointment_AgreeSerializer(serializers.ModelSerializer):
    appointment_sub = InterviewSub_AppointmentSerializer(required=True)
    class Meta:
        model = InterviewSub_Appointment_Agree
        fields = (
            'appointment_sub',
            'date',
            'contact',
            'address',
            'postname',
            'certification',
            'attention',
            'first_impression',
            'notes',
        )

    def create(self, validated_data):
        appointment_sub_data = validated_data.pop('appointment_sub')

        appointment_sub_ = InterviewSub_AppointmentSerializer.create(InterviewSub_AppointmentSerializer(),
                                                                     validated_data=appointment_sub_data)
        appointment_sub_agree, created = InterviewSub_Appointment_Agree.objects.update_or_create(
            appointment_sub=appointment_sub_,
            **validated_data)
        # update interview table

        interview = Interview.objects.get(pk=appointment_sub_.interview.id)
        interview.status = 3
        interview.save()

        return appointment_sub_agree

# Interview Result SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------
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
    interview_sub = InterviewSub_InterviewSerializer(required=True)
    class Meta:
        model = InterviewSub_Interview_Pass
        fields = (
            'interview_sub',
            'reason',
            'description',
            'comments',
            'notes',
        )

    def create(self, validated_data):
        interview_sub_data = validated_data.pop('interview_sub')
        interview_sub_ = InterviewSub_InterviewSerializer.create(InterviewSub_InterviewSerializer(),
                                                                validated_data=interview_sub_data)

        interview_sub_pass, created = InterviewSub_Interview_Pass.objects.update_or_create(
            interview_sub=interview_sub_,
            **validated_data)

        # update interview table
        interview = Interview.objects.get(pk=interview_sub_.interview.id)
        interview.status = 4
        interview.save()

        return interview_sub_pass

# Interview Offer SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------
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
    offer_sub = InterviewSub_OfferSerializer(required=True)
    class Meta:
        model = InterviewSub_Offer_Agree
        fields = (
            'offer_sub',
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
        offer_sub_data = validated_data.pop('offer_sub')

        offer_sub_ = InterviewSub_OfferSerializer.create(InterviewSub_OfferSerializer(),
                                                        validated_data=offer_sub_data)

        offer_sub_agree, created = InterviewSub_Offer_Agree.objects.update_or_create(
            offer_sub=offer_sub_,
            **validated_data)

        # update interview table
        interview = Interview.objects.get(pk=offer_sub_.interview.id)
        interview.status = 5
        interview.save()

        return offer_sub_agree
