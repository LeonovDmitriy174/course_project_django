import smtplib
from django.core.mail import send_mail
from datetime import datetime, timedelta
import pytz
from config import settings
from mailing.models import MailingSettings, MailingStatus, LOGS_STATUS_CHOICES, MailingMessage
from django.core.cache import cache

from client.models import Client
from config.settings import CACHE_ENABLED


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)

    mailings = MailingSettings.objects.filter(first_datetime__lte=current_datetime).filter(
        setting_status__in=['Create'])

    for mailing in mailings:
        title = mailing.message.title
        content = mailing.message.content
        mailing.setting_status = 'Started'
        mailing.save()
        try:
            server_response = send_mail(
                subject=title, message=content, from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in mailing.clients.all()], fail_silently=False)
            if server_response == 1:
                server_response = 'Письмо успешно отправлено'
                MailingStatus.objects.create(status=LOGS_STATUS_CHOICES[0][1], mailing_response=server_response,
                                             mailing=mailing)

            mailing.setting_status = 'Create'

            if mailing.sending == 'daily' and server_response == 1:
                current_datetime = MailingSettings.objects.get(sending='daily')
                mailing.first_datetime = current_datetime.first_datetime + timedelta(days=1)
                mailing.setting_status = 'Create'

            elif mailing.sending == 'weekly' and server_response == 1:
                current_datetime = MailingSettings.objects.get(sending='weekly')
                mailing.first_datetime = current_datetime.first_datetime + timedelta(days=7)
                mailing.setting_status = 'Create'

            elif mailing.sending == 'monthly' and server_response == 1:
                current_datetime = MailingSettings.objects.get(sending='monthly')
                mailing.first_datetime = current_datetime.first_datetime + timedelta(days=30)
                mailing.setting_status = 'Create'

            mailing.save()

        except smtplib.SMTPException as error:
            MailingStatus.objects.create(status=LOGS_STATUS_CHOICES[1][1], mailing_response=error,
                                         mailing=mailing)
            mailing.setting_status = 'Create'


def get_mailings_from_cache():
    """Получает список клиентов из кэша, если он пустой получает из базы данных"""
    if not CACHE_ENABLED:
        return MailingSettings.objects.all()
    key = 'client_list'
    mailings = cache.get(key)
    if mailings is not None:
        return mailings
    mailings = MailingSettings.objects.all()
    cache.set(key, mailings)
    return mailings


def get_messages_from_cache():
    """Получает список клиентов из кэша, если он пустой получает из базы данных"""
    if not CACHE_ENABLED:
        return MailingMessage.objects.all()
    key = 'client_list'
    messages = cache.get(key)
    if messages is not None:
        return messages
    messages = MailingMessage.objects.all()
    cache.set(key, messages)
    return messages