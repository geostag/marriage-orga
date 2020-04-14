from django import forms
from backend.models import Document

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('file',"notes","event")
        widgets = {
            'notes':  forms.Textarea(attrs={'class':'form-control','rows':4}),
            'file':   forms.ClearableFileInput(attrs={'class':'NOTform-control'}),
            'event':  forms.HiddenInput(attrs={'class':'form-control'}),
        }
        labels = {
            "file":      "Dokument",
            "notes":     "Bemerkungen",
            "event": "",
        }

