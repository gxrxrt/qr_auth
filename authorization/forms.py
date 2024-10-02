from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(max_length=100, label='Login')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
