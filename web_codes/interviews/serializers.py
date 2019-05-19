from rest_framework import serializers

from .models import Interview

class InterviewSerializer(serializers.ModelSerializer):
#    post_id = serializers.RelatedField(source='post', read_only=True)
    class Meta:
        model = Interview
        fields = (
            'resume',
            'post',
            'is_active',
            'status',
            'result',
        )
