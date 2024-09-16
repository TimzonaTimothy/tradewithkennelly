from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
    }))
    class Meta:
        
        model = Account
        fields = ['first_name', 'last_name','bitcoin_address', 'email', 'password',]

    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match!'
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['bitcoin_address'].widget.attrs['placeholder'] = 'Your Bitcoin Wallet Address'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserForm(forms.ModelForm):
    # profile_picture = forms.ImageField(required=False, error_messages = {'invalid':('Image files only')}, widget=forms.FileInput)
    class Meta:
        model = Account
        fields = ('first_name', 'last_name','bitcoin_address','state','email','username','country', )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



