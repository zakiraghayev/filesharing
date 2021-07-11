from rest_framework import viewsets, response, permissions, decorators
from .serializers import FileContainerSerializer, FileContainer

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