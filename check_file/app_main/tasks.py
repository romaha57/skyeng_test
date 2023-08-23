import logging

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q

from app_main.models import UploadFile
from app_main.utils import check_linter_file

logger = logging.getLogger('main_logger')


@shared_task
def check_files() -> None:
    """Отложенная задача celery для проверки новых/перезаписанных файлов в системе """

    new_overwritten_files = UploadFile.objects.filter(Q(status__in=['new', 'overwritten']) & Q(is_check=False))

    for new_overwritten_file in new_overwritten_files:

        # проверка файла
        message_text = check_linter_file(file_path=new_overwritten_file.file)

        logger.info(f'Проверен файл {new_overwritten_file.file}')
        send_email_after_check.delay(user_id=new_overwritten_file.user.id,
                                     record_id=new_overwritten_file.id,
                                     message_text=message_text)


@shared_task
def send_email_after_check(user_id: int, record_id: int, message_text: str) -> None:
    """Отложенная таска для отправки письма на почту и обновление данных о файле"""

    user = User.objects.get(pk=user_id)
    upload_file = UploadFile.objects.get(pk=record_id)

    updated_at = upload_file.updated_at.strftime('%d.%m.%Y %H:%M')
    filename = str(upload_file.file.name).split('/')[-1]

    send_mail(
        subject=f'Отчет о проверке вашего файла {filename} загруженный в {updated_at}',
        message=message_text,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )

    upload_file.update_after_check(message_text=message_text)

    logger.info(f'Письмо с отчетом после проверки отправлено на {user.email}')
