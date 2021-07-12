# Import models
from core.models import FileContainer, PermType
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages

# import rest framework
from rest_framework import fields, serializers


class FileContainerSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    nofshared = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    
    class Meta:
        model = FileContainer
        fields = ["id", "name", "desc", "file", "username", "nofshared"]
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        messages.success(self.context["request"], 'File uploaded successfuly. Please, look at my files section below.')
        return super().create(validated_data)

    def get_username(self, obj):
        return obj.owner.username
    
    def get_nofshared(self, obj):
        return obj.permissions.count()
    
    def get_id(self, obj):
        return obj.id

class PermTypeSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username")
    class Meta:
        model = PermType
        fields = ["perm", "username"]

    def create(self, validated_data):
        uname = validated_data.get("user")['username']
        
        owner = self.context['request'].user
        file2share = get_object_or_404(owner.myfiles.all(), pk=self.context['file'])
        share2whom = get_object_or_404(User, username=uname)
        perm, _ = file2share.permissions.get_or_create(user = share2whom)
        perm.perm =  validated_data.get("perm")
        perm.save()
        return validated_data
