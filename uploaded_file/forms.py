from django import forms
from .models import UploadedFile
from pathlib import Path

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ["file"]

    def clean_file(self):
        file = self.cleaned_data["file"]

        allowed_extensions = [
            ".csv",
            ".xlsx",
            ".xls"
        ]

        extension =  Path(file.name).suffix.lower()

        if extension not in allowed_extensions:
            raise forms.ValidationError("Only CSV and Excel allowed.")
        return file