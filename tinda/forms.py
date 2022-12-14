from django.forms import ModelForm
from django import forms
from tinda.models import TindaDates, UploadModel, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
import datetime


class NewTinda(forms.ModelForm):
    date_of_birth=forms.DateTimeField(widget=forms.DateInput(attrs={'class':'datepicker'}))
    class Meta:
        model=TindaDates
        fields='__all__'
        

class UploadForm(ModelForm):
    class Meta:
        model=UploadModel
        fields="__all__"

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name', 'email', 'username', 'password1', 'password2']
        label={
            'first_name':'Name',
        }

class CommentForm(ModelForm):
    post = forms.ModelChoiceField(queryset=UploadModel.objects.all())
    class Meta:
        model=Comment
        fields=['post','text']
