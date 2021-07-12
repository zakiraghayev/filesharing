from django.urls import path
from django.urls.conf import include
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("detail/<int:pk>", DetailView.as_view(), name="detail"),
    path("login", LoginView.as_view()),
    
    path("accounts/register/", RegistrationView.as_view()),
    path("accounts/profile/", ProfileViewRedirect.as_view()),
    path("api/", include("core.api.urls")),
]