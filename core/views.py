from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView, RedirectView
from django.urls import reverse_lazy

from django_registration.views import RegistrationView as BaseRegistrationView
from .models import FileContainer

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

class DetailView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    redirect_field_name = 'redirect_to'

    template_name = "core/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk, user = kwargs.get("pk", 0), self.request.user
        file = None
        try:
            file = get_object_or_404(user.myfiles, pk=pk)
        
        except:
            try:
                files = FileContainer.objects.filter(permissions__in =  user.myperm.all())
                file = files.get(pk=pk)

            except:
                file = None

        context['file'] = file
        return context

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
