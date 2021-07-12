from django.db.models import fields
from core.models import FileContainer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, response, permissions, decorators
from rest_framework import serializers
from .serializers import FileContainerSerializer, PermTypeSerializer, CommentSerializer

# Views API

class FileContainerApi(viewsets.ModelViewSet):

    serializer_class = FileContainerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Returns shared files """
        myperms = self.request.user.myperm.all()
        return [f.filesshared.first() for f in myperms]
    
    @decorators.action(detail=False, methods=['get'])
    def myfiles(self, request):
        queryset = request.user.myfiles.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)
    
    @decorators.action(detail=True, methods=['post'])
    def shareWith(self, request, pk=None):
        print(request.data)
        serializer = self.get_serializer_class()(data=request.data, \
            context={"request":request, "file":pk}, many=False)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors)

    def get_serializer_class(self):
        if self.action == "shareWith":
            return PermTypeSerializer
        return super().get_serializer_class()

class CommentsAPI(viewsets.ViewSet):

    def get(self, request, pk=None):
        myperm = request.user.myperm.filter(perm=True)
        file = get_object_or_404(FileContainer.objects.filter(permissions__in = myperm)\
            , pk=pk)
        data = CommentSerializer(file.comments.all(), many=True).data
        return response.Response(data)
        