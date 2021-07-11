# Import models
from core.models import FileContainer

# import rest framework
from rest_framework import fields, serializers


class FileContainerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    nofshared = serializers.SerializerMethodField()
    class Meta:
        model = FileContainer
        fields = ["name", "desc", "file", "username", "nofshared"]
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def get_username(self, obj):
        return obj.owner.username
    
    def get_nofshared(self, obj):
        return obj.permissions.count()