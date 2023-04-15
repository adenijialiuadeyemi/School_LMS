from django import forms
from django.contrib.auth.models import User
from .models import userProfileInfo
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = [
            ('password1','Password'),
            ('password2','Confirm Password')
        ]

class UserProfileInfoForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    user_types = [('Student','Student'), ('Parent','Parent')]
    user_type = forms.ChoiceField(choices=user_types)
    class Meta:
        model = userProfileInfo
        fields = ('bio', 'profile_pics', 'user_type')