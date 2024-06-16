from django.contrib import admin

from mailing.models import MailingSettings, MailingMessage

admin.site.register(MailingSettings)
admin.site.register(MailingMessage)
