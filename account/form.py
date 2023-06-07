from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import CustomUser
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _



class UserAdminform(UserCreationForm):
    

    class Meta:
        model= get_user_model()
        fields=["username", "first_name", "last_name","email", "phone_number","nationality"]

    def clean_email(self):
        email_check= self.cleaned_data.get('email')
        
        check_unique_email=CustomUser.objects.filter(email=str(email_check).lower())
        
        if check_unique_email:
            raise forms.ValidationError('email already exist choose another email')
        return email_check


class Setpassword(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)


    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2


class UserAdminform(UserCreationForm):
    

    class Meta:
        model= get_user_model()
        fields=["username", "first_name", "last_name","email", "phone_number","nationality"]