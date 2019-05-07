from rest_framework import serializers

from .models import Interview

class InterviewSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    candidate_name = serializers.SerializerMethodField()
    post_name = serializers.SerializerMethodField()

    def get_id(self, interview):
        return interview.id

    def get_candidate_name(self, interview):
        return interview.candidate.resume_set.first().username

    def get_post_name(self, interview):
        return interview.post.name

    class Meta:
        model = Interview
        fields = (
            'id',
            'candidate_name',
            'post_name',
            'is_active',
            'status',
            'result',
            )
