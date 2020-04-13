# coding=utf-8
from django import forms

class EnterForm(forms.Form):
    shortcut = forms.CharField(label='',required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Eventname'}))
    password = forms.CharField(label='',required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Passwort'}))

class EnterWithCodeForm(forms.Form):
    partcode = forms.CharField(label='',required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Teilnahmeccode'}))
