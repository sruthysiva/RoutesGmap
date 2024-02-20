from django import forms
from django.core.exceptions import ValidationError
from .models import UploadedFile
from django.contrib.auth.forms import *


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed_extensions = ['.csv', '.xls', '.xlsx']
            if not any(file.name.endswith(ext) for ext in allowed_extensions):
                raise ValidationError('Invalid file type. Please upload a CSV or Excel file.')
            
        return file
    
