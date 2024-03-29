# coding=utf-8
from django import forms
from django.utils.translation import gettext as _

class EnterForm(forms.Form):
    shortcut = forms.CharField(label='',required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':_('Eventname')}))
    password = forms.CharField(label='',required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':_('Passwort')}))

class EnterWithCodeForm(forms.Form):
    partcode = forms.CharField(label='',required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':_('Teilnahmecode')}))

class CodeForgottenForm(forms.Form):
    email = forms.CharField(label='',required=True,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':_('E-Mail')}))
