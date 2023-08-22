import os

from django import forms
from django.core.exceptions import ValidationError

from .models import UploadFile


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFile
        fields = ('file', )

    def clean_file(self):
        """Проверка на расширение загружаемого файла"""

        filename = self.cleaned_data["file"]
        file_extensions = filename.name.split('.')[-1]
        if file_extensions != 'py':
            raise ValidationError('Можно загружать только файлы с расширением .py')

        return filename

    def save(self, commit=True):
        print(self.instance.status)
        if self.instance.status == 'new' and os.path.exists(f'media/{self.instance}') and str(self.instance).split('/')[-1] == str(self.cleaned_data.get('file')):
            os.remove(f'media/{self.instance}')
            self.instance.status = 'overwritten'

        super().save(commit=True)
