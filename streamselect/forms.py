from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django.core.exceptions import ValidationError

from .models import userbasicinfo

# create a ModelForm
class ProfileForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = userbasicinfo
        #fields = '__all__'
        exclude = ['user_id']


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
