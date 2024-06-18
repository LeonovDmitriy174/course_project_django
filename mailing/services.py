import smtplib
from django.core.mail import send_mail
from datetime import datetime, timedelta
import pytz
from config import settings
from mailing.models import MailingSettings, MailingStatus, LOGS_STATUS_CHOICES, MailingMessage
from django.core.cache import cache
from client.models import Client
from config.settings import CACHE_ENABLED
from dateutil.relativedelta import relativedelta

def get_mailings_from_cache():
    """Получает список рассылок из кэша, если он пустой получает из базы данных"""
    if not CACHE_ENABLED:
        return MailingSettings.objects.all()
    key = 'mailing_list'
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = MailingSettings.objects.all()
    cache.set(key, mailings)
    return mailings


def get_messages_from_cache():
    """Получает список сообщений из кэша, если он пустой получает из базы данных"""
    if not CACHE_ENABLED:
        return MailingMessage.objects.all()
    key = 'message_list'
    messages = cache.get(key)
    if messages is not None:
        return messages
    messages = MailingMessage.objects.all()
    cache.set(key, messages)
    return messages


def send_mailing():
    """Функция отправки письма"""
    # Определяем текущее время
    zone = pytz.timezone(settings.TIME_ZONE)
    current_time = datetime.now(zone)

    # Собираем рассылки, которые необходимо отправить
    mailing_settings = MailingSettings.objects.filter(next_datetime__lte=current_time).filter(
        setting_status__in=['Create', 'Started'])
    for mailing in mailing_settings:
        # Устанавливаем время следующей рассылки, если оно еще не определено
        if mailing.next_datetime is None:
            mailing.next_datetime = current_time
        # Подготавливаем данные для отправки письма
        title = mailing.message.title
        content = mailing.message.content
        mailing.setting_status = 'Started'
        mailing.save()
        try:
            # Проверяем, не истекло ли время рассылки
            if mailing.end_time < mailing.next_datetime:
                mailing.next_datetime = current_time
                mailing.settings_status = 'Done'
                mailing.save()
                continue
            # Проверяем, требуется ли отправить рассылку
            if mailing.next_datetime <= current_time:
                # Отправляем письмо
                server_response = send_mail(
                    subject=title,
                    message=content,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.clients.all()],
                    fail_silently=False,
                )
                if server_response == 1:
                    server_response = 'Сообщение отправлено'
                # Создаем модель статуса рассылки
                MailingStatus.objects.create(status='success', mailing_response=server_response, mailing=mailing)

                # Определяем время следующей рассылки
                if mailing.sending == 'Daily':
                    mailing.next_datetime = current_time + timedelta(days=1)

                elif mailing.sending == 'Weekly':
                    mailing.next_datetime = current_time + timedelta(days=7)

                elif mailing.sending == 'Monthly':
                    mailing.next_datetime = current_time + relativedelta(months=1)

            mailing.save()

        except smtplib.SMTPException as error:
            MailingStatus.objects.create(status='fail', mailing_response=error, mailing=mailing)