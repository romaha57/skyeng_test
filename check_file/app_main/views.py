import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView

from app_users.mixins import TitleMixin

from .forms import UploadFileForm
from .models import UploadFile


class IndexView(TitleMixin, TemplateView):
    """Главная страница"""

    template_name = 'app_main/index.html'
    title = 'Главная'


class UploadFileView(TitleMixin, LoginRequiredMixin, CreateView):
    """Страница загрузки файла и отчета по проверкам"""

    model = UploadFile
    template_name = 'app_main/upload-file.html'
    title = 'Загрузка файла'
    form_class = UploadFileForm

    def form_valid(self, form):
        """Добавляем user в форму """

        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:upload_file')


class DeleteFile(LoginRequiredMixin, View):
    """Удаление записи о загрузке файла"""

    def get(self, request, pk):
        file = UploadFile.objects.get(pk=pk)

        # удаляем сам файл с сервера
        if os.path.exists(f'media/{file.file}'):
            os.remove(f'media/{file.file}')

        file.status = 'deleted'
        file.save()
        return redirect('main:upload_file')
