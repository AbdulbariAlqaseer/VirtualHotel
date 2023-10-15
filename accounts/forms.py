from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms.widgets import Widget

from accounts.models import Account

class RegistrationForm(UserCreationForm):
    email =forms.EmailField(max_length=60, help_text='Required, add a valid E-mail address')
    first_name=forms.CharField(help_text='Required')
    last_name=forms.CharField(help_text='Required')
    birth_date=forms.DateField(help_text='Date Of Birth',widget=forms.DateInput())
    class Meta:
        model=Account
        fields =("email","first_name", "last_name","password1","password2")

class StaffRegistrationForm(UserCreationForm):
    email =forms.EmailField(max_length=60, help_text='Required, add a valid E-mail address',widget=forms.EmailInput(attrs={'class':'floatLabel'}))
    first_name=forms.CharField(help_text='Required',widget=forms.TextInput(attrs={'class':'floatLabel'}))
    last_name=forms.CharField(help_text='Required',widget=forms.TextInput(attrs={'class':'floatLabel'}))
    password1 = forms.CharField(help_text = 'Required',widget=forms.PasswordInput(attrs={'class':'floatLabel'}))
    password2 = forms.CharField(help_text = 'Required, Confirm Password',widget=forms.PasswordInput(attrs={'class':'floatLabel'}))
    address=forms.CharField(help_text='Employee Address',widget=forms.TextInput(attrs={'class':'floatLabel'}))
    class Meta:
        model=Account
        fields =("email","first_name", "last_name","password1","password2")

class AccountAuthenticationForm(forms.ModelForm):

    # password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model=Account
        fields=('email','password')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                }),
            'password': forms.PasswordInput(attrs={
                'class': "form-control", 
                'style': 'max-width: 300px;',
                'placeholder': 'Password'
            })
        }

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid Login")