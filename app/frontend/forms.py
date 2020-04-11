# coding=utf-8
from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe

class LoginForm(forms.Form):
    username = forms.CharField(label='Email',required=True,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email-Adresse'}))
    password = forms.CharField(label='Passwort',required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Passwort'}))

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Vorname',required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Vorname'}))
    last_name  = forms.CharField(label='Nachname',required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nachname'}))
    email      = forms.EmailField(label='Email',required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email-Adresse'}))
    password   = forms.CharField(label='Passwort',required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Passwort'}))
    password2  = forms.CharField(label='Passwort wiederholen',required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Passwort'}))
    dsconfirm = forms.BooleanField(
        #label=mark_safe('Ich habe die <a href="%s">Datenschutzerklärung</a> zur Kenntnis genommen' % +reverse(v2.views.rendertemplate, kwargs={"template":"v2/datenschutz.html"})),
        label=mark_safe('Ich habe die <a href="../../v2/render/v2/datenschutz.html">Datenschutzerklärung</a> zur Kenntnis genommen' ),
        widget=forms.CheckboxInput(),
        error_messages={'required': u'Bitte die Kenntnisnahme der Datenschutzerklärung bestätigen.'},
        required = True
    )
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password  = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError( "Die Passwörter stimmen nicht überein" )
 
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='',required=True,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email-Adresse'}))
    
class PasswordChangeForm(forms.Form):
    password  = forms.CharField(label='Passwort',required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Passwort'}))
    password2 = forms.CharField(label='Passwort wiederholen',required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Passwort'}))
    
    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        password  = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError( "Die Passwörter stimmen nicht überein" )
