from django import forms
from django.contrib.auth.models import User
import django_countries
import datetime
from models import pushitem, UserProfile
from language_constants import *
from salcat.registration_backend import SalcatRegistrationForm
from django.utils.translation import ugettext as _

class UserForm(forms.ModelForm):
    class Meta:
        model = User        
        exclude = ('first_name','last_name','timestamp','date_joined',
                   'last_login','is_staff','is_active','is_superuser',
                   'groups','user_permissions')

class pushitemForm(forms.ModelForm):
    title = forms.CharField(max_length=150, required=True,label=LANGUAGE['PushTitle'])
    background= forms.CharField(label=LANGUAGE['Background'],required=False,
                widget = forms.Textarea(attrs={'cols': 80, 'rows': 10})
                    )
    tag = forms.SelectMultiple(choices=['a','b','c'])
    class Meta:
        model = pushitem
        fields = ('title','background')

class tagForm(forms.Form):
    tag = forms.CharField()

class commentForm(forms.ModelForm):
    class Meta:
        model = pushitem
        fields = ('background',)
    background= forms.CharField(label=LANGUAGE['CommentBody'],
                widget = forms.Textarea(attrs={'cols': 80, 'rows': 20})
                    )

class UserProfileForm(forms.ModelForm):
    """Use for editing user profile."""
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = UserProfile
        exclude = ('user', 'dob')

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data is None or data == '':
            raise forms.ValidationError(_("This field is required."))

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data is None or data == '':
            raise forms.ValidationError(_("This field is required."))

        # Always return the cleaned data, whether you have changed it or
        # not.
        return data

    def save(self, commit=True):
        data = forms.ModelForm.save(self, False)
        data.user.first_name = self.cleaned_data['first_name']
        data.user.last_name = self.cleaned_data['last_name']
        if commit:
            data.save()
            data.user.save()
        return data
