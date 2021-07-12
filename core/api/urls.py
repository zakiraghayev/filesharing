from django.urls.conf import path
from rest_framework.routers import DefaultRouter
from .views import FileContainerApi, CommentsAPI

router = DefaultRouter()
router.register(r'files', FileContainerApi, basename='files')
urlpatterns = router.urls

urlpatterns += [
    path("filecomments/<int:pk>", CommentsAPI.as_view({"get":"get"}), name="comments")
]