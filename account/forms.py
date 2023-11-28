from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegestrationForm(forms.Form):
    username=forms.CharField(widget=forms.Textarea)
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='password' , widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' 452'}))
    password2=forms.CharField(label='confirm password' ,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':' 452'}))

    def clean_email(self):

        email = self.cleaned_data['email']        
        user = User.objects.filter(email = email).exists()
        if user:
            raise ValidationError('your email is already exist ')
        
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('password must match')
        

class UserLoginForm(forms.Form):
    username=forms.CharField(widget=forms.Textarea)
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

