from django.contrib.auth.models import User
from django.db import models


def path_for_upload_file(instance, filename):
    """Путь для загрузки файлов"""

    return f'{instance.user.email}/{filename}'


STATUSES_UPLOAD_FILE = (
    ('new', 'новый'),
    ('overwritten', 'перезаписан'),
    ('deleted', 'удален')
)


class UploadFile(models.Model):
    """Модель загруженного файла"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', verbose_name='пользователь')
    file = models.FileField(upload_to=path_for_upload_file, verbose_name='файл')
    status = models.CharField(max_length=20, choices=STATUSES_UPLOAD_FILE, verbose_name='статус', default='new')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='время обновления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='время создания')
    is_check = models.BooleanField(default=False, verbose_name='проверено')
    is_right = models.BooleanField(verbose_name='правильно выполнено', null=True, blank=True)

    def filename(self):
        """Название файла"""

        return self.file.name.split('/')[-1]

    class Meta:
        verbose_name = 'загруженный файл'
        verbose_name_plural = 'загруженные файлы'
        ordering = ('-updated_at',)

    def __str__(self):
        return f'{self.user.email}/{self.file}'

    def update_after_check(self, message_text: str):
        """Изменения полей файла в БД после проверки его """

        # отмечаем правильность выполнения файла
        if 'успешно' in message_text:
            self.is_right = True
        else:
            self.is_right = False

        # отмечаем что файл проверен
        self.is_check = True
        self.save()
