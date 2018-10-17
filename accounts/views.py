from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.db import transaction
from django.core.mail import EmailMessage

from .forms import ManagerSignUpForm, CustomerSignUpForm
from .models import User
from .emails import MANAGER_JOIN_EMAIL

class index(TemplateView):
    template_name= 'registration/homepage.html'

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'

class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        # login(self.request, user)
        admin_email = User.objects.get(pk=1).email
        subject = "[YOYO] New Manager - %s" % user.username
        body = MANAGER_JOIN_EMAIL % (user.username, user.manager.hotel)
        # try:
        email = EmailMessage(subject, body, to=[admin_email])
        email.send()
        user.save()
        # except:
            # print("Unable to send email (%s)" % admin_email)
        return redirect('hotels:hotel-list')

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('hotels:hotel-list')