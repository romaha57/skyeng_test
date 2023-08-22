import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, DeleteView

from .forms import UploadFileForm
from .models import UploadFile
from app_users.mixins import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'app_main/index.html'
    title = 'Главная'


class UploadFileView(TitleMixin, LoginRequiredMixin, CreateView):
    model = UploadFile
    template_name = 'app_main/upload-file.html'
    title = 'Загрузка файла'
    form_class = UploadFileForm

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:upload_file')


class DeleteFile(LoginRequiredMixin, View):
    def get(self, request, pk):
        file = UploadFile.objects.get(pk=pk)
        if os.path.exists(f'media/{file.file}'):
            os.remove(f'media/{file.file}')

        file.status = 'deleted'
        file.save()
        return redirect('main:upload_file')







