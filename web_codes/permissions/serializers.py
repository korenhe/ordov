from rest_framework import serializers
from .models import ProjectPermission

# Attention: the resume serializer should be 
# TODO: The Permission DB only
class ProjectPermissionSerializer(serializers.ModelSerializer):

    post_id = serializers.SerializerMethodField()
    post_name = serializers.SerializerMethodField()
    stage_id = serializers.SerializerMethodField()
    stage_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_post_id(self, projPerm):
        return projPerm.post.id
    def get_post_name(self, projPerm):
        return projPerm.post.name
    def get_stage_id(self, projPerm):
        return projPerm.stage
    def get_stage_name(self, projPerm):
        return projPerm.user.user.name
    def get_user_name(self, projPerm):
        return projPerm.user.user.name
    def get_user_id(self, projPerm):
        return projPerm.user.id

    class Meta:
       model = ProjectPermission
       fields = (
         'post_id',
         'post_name',
         'stage_id',
         'stage_name',
         'user_name',
         'user_id',
       )

