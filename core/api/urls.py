from rest_framework.routers import DefaultRouter
from .views import FileContainerApi

router = DefaultRouter()
router.register(r'files', FileContainerApi, basename='files')
urlpatterns = router.urls