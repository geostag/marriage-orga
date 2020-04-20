from django import forms
from backend.models import Document, Coli

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('file',"notes","event","public")
        widgets = {
            'notes':  forms.Textarea(attrs={'class':'form-control','rows':4}),
            'file':   forms.ClearableFileInput(attrs={'class':'NOTform-control'}),
            'event':  forms.HiddenInput(attrs={'class':'form-control'}),
            'public': forms.CheckboxInput(attrs={'class':'form-check-label'}),
        }
        labels = {
            "file":      "Dokument",
            "notes":     "Bemerkungen",
            "event":     "",
            "public":    "Öffentlich",
        }

class ColiForm(forms.ModelForm):
    
    class Meta:
        model = Coli
        fields = ('name',"url","image","notes","checkoutlist")
        widgets = {
            'name':   forms.TextInput(attrs={'class':'form-control'}),
            'url':    forms.URLInput(attrs={'class':'form-control'}),
            'notes':  forms.Textarea(attrs={'class':'form-control','rows':4}),
            'image':  forms.ClearableFileInput(attrs={'class':'NOTform-control'}),
            'checkoutlist':  forms.HiddenInput(attrs={'class':'form-control'}),
        }
        labels = {
            "name":      "Titel",
            "url":       "Weblink",
            "notes":     "Text",
            "image":     "Bild",
            "checkoutlist":     "",
        }
    
    