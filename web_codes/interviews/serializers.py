from rest_framework import serializers

from .models import Interview, Offer

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
