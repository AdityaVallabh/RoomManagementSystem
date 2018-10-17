from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from hotels.models import Hotel
from .models import User, Manager, Customer

class ManagerSignUpForm(UserCreationForm):
    hotel = forms.ModelChoiceField(
        queryset=Hotel.objects.all(),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_manager = True
        user.save()
        student = Manager.objects.create(user=user, hotel=self.cleaned_data.get('hotel'))
        return user

class CustomerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
            student = Customer.objects.create(user=user)
        return user
