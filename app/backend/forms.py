from django import forms
from backend.models import Document

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

