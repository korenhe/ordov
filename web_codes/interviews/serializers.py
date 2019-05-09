from rest_framework import serializers

from .models import Interview

class InterviewSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    candidate_name = serializers.SerializerMethodField()
    post_name = serializers.SerializerMethodField()

    def get_id(self, interview):
        return interview.id

    def get_candidate_name(self, interview):
        try:
            return interview.candidate.resume_set.first().username
        except AttributeError:
            return "Anonymous"

    def get_post_name(self, interview):
        return interview.post.name

    class Meta:
        model = Interview
        fields = (
            'id', #M
            'candidate_name', #M
            'post_name', #M
            'candidate',
            'post',
            'is_active',
            'status',
            'result',
        )
