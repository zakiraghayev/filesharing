from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from django.urls import reverse_lazy

from django_registration.views import RegistrationView as BaseRegistrationView

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    template_name = "core/index.html"


class LoginView(TemplateView):
    template_name = "core/login.html"

class ProfileViewRedirect(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'home'

class RegistrationView(BaseRegistrationView):
    """
    
    """

    email_body_template = "django_registration/activation_email_body.txt"
    email_subject_template = "django_registration/activation_email_subject.txt"
    success_url = reverse_lazy("home")

    def register(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = True
        new_user.save()
        return new_user
