from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . models import ShopCart



class RegistrationForm(UserCreationForm):
    class Meta:
        model= User
        fields = ('username','first_name','last_name','email','password1','password2')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control'}),
        }



        class ShopCartForm(forms.ModelForm):
            class Meta:
                model = ShopCart()
                fields = ('quantity',)