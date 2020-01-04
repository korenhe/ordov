from rest_framework import serializers

from .models import Interview
from .models import InterviewLogCommon
from resumes.models import Resume

from .models import InterviewSub_Appointment, InterviewSub_Appointment_Agree
from .models import InterviewSub_Interview, InterviewSub_Interview_Pass
from .models import InterviewSub_Offer, InterviewSub_Offer_Agree
from .models import InterviewSub_Probation, InterviewSub_Probation_Fail
from .models import InterviewSub_Payback, InterviewSub_Payback_Finish
from .models import InterviewSub_Terminate
from .models import STATUS_CHOICES

from django.core.exceptions import MultipleObjectsReturned

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
            'sub_status',
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
            'date',
            'contact',
            'address',
            'postname',
            'certification',
            'attention',
            'first_impression',
            'notes',
        )

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
            'comments',
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
        interview.sub_status = 'OFFER'
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

        # Attention: The Interview - Offer - Offer_Agree is one-one-one relationship
        offer_sub_ = InterviewSub_Offer.objects.all().filter(interview_id=offer_sub_data.get('interview'))
        if offer_sub_ is None or len(offer_sub_) is 0:
            offer_sub_ = InterviewSub_OfferSerializer.create(InterviewSub_OfferSerializer(), validated_data=offer_sub_data)
        else:
            offer_sub_ = offer_sub_[0]

        offer_sub_agree = None
        try:
            offer_sub_agree, created = InterviewSub_Offer_Agree.objects.update_or_create(
                offer_sub_id=offer_sub_.id, defaults=validated_data)
        except (MultipleObjectsReturned):
            # To walkaround the perious bug
            # Attention! The Interview - Offer - Offer_Agree is one-one-one relationship
            offer_agree_subs = InterviewSub_Offer_Agree.objects.all().filter(offer_sub_id=offer_sub_.id)
            """
            FixUp all the offer_subs
            """
            offerAgreeSeri = InterviewSub_Offer_AgreeSerializer()
            for oas in offer_agree_subs:
                item = offerAgreeSeri.update(
                        instance=oas,
                        validated_data=validated_data
                )
                item.save()
                offer_sub_agree = item

        return offer_sub_agree

# Interview Probation SubModal

# ---------------------------------------- Pretty Split Line ----------------------------------------
class InterviewSub_ProbationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSub_Probation
        fields = (
            'interview',
            'result_type',
        )

class InterviewSub_Probation_FailSerializer(serializers.ModelSerializer):
    probation_sub = InterviewSub_ProbationSerializer(required=True)
    class Meta:
        model = InterviewSub_Probation_Fail
        fields = (
            'probation_sub',

            'reason',
            'comments',
        )

    # Negative so no need to update status, but need to update is_active
    def create(self, validated_data):
        probation_sub_data = validated_data.pop('probation_sub')

        probation_sub_ = InterviewSub_ProbationSerializer.create(InterviewSub_ProbationSerializer(),
                                                        validated_data=probation_sub_data)

        probation_sub_fail, created = InterviewSub_Probation_Fail.objects.update_or_create(
            probation_sub=probation_sub_,
            **validated_data)

        # update interview table
        interview = Interview.objects.get(pk=probation_sub_.interview.id)
        interview.is_active = False
        interview.sub_status = STATUS_CHOICES[interview.status][1]+"-终止"
        interview.save()

        return probation_sub_fail

# Interview Payback SubModal
# ---------------------------------------- Pretty Split Line ----------------------------------------

class InterviewSub_PaybackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSub_Payback
        fields = (
            'interview',
            'result_type',
        )

class InterviewSub_Payback_FinishSerializer(serializers.ModelSerializer):
    payback_sub = InterviewSub_PaybackSerializer(required=True)
    class Meta:
        model = InterviewSub_Payback_Finish
        fields = (
            'payback_sub',
            'notes',
        )

    def create(self, validated_data):
        payback_sub_data = validated_data.pop('payback_sub')

        payback_sub_ = InterviewSub_PaybackSerializer.create(InterviewSub_PaybackSerializer(),
                                                             validated_data=payback_sub_data)

        payback_sub_finish, created = InterviewSub_Payback_Finish.objects.update_or_create(
            payback_sub=payback_sub_,
            **validated_data)

        # update interview table
        interview = Interview.objects.get(pk=payback_sub_.interview.id)
        interview.status = 8
        interview.sub_status = '完成'
        interview.save()

        return payback_sub_finish

# Interview Terminate SubModal
class InterviewSub_TerminateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSub_Terminate
        fields = (
            'interview',

            'expected_industry',
            'expected_post',
            'expected_shift',
            'expected_salary',

            'expected_notes',

            'expected_province',
            'expected_city',
            'expected_district',

            'expected_insurance',
            'expected_insurance_schedule'
        )

    def create(self, validated_data):
        # This is an example for override the default create behavior
        terminate_sub = InterviewSub_Terminate.objects.create(**validated_data)

        # update interview table
        interview = Interview.objects.get(pk=terminate_sub.interview.id)

        # we should update the status info to resumes
        """
        resume = None
        try:
            resume = Resume.objects.get(pk=interview.resume_id)
        except:
            pass
        if resume is not None:
            resume.expected_province = validated_data.get("expected_province", "")
            resume.expected_city = validated_data.get("expected_city", "")
            resume.expected_district = validated_data.get("expected_district", "")
            resume.save()
        """

        interview.is_active = False
        interview.sub_status = STATUS_CHOICES[interview.status][1]+"-终止"
        interview.save()

        return terminate_sub
