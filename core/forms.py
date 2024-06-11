from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client, Company

class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'password1', 'password2')

class CompanyRegistrationForm(UserCreationForm):
    class Meta:
        model = Company
        fields = ('email', 'password1', 'password2', 'name', 'category')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-emerald-600 focus:border-emerald-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-emerald-500 dark:focus:border-emerald-500', 'required': 'true'})
