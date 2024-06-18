from django import forms

from client.models import Client
from mailing.models import MailingSettings, MailingMessage
from users.forms import StileFormMixin


class MailingSettingsForm(StileFormMixin, forms.ModelForm):
    """Форма для создания статьи"""
    def __init__(self, *args, **kwargs):
        """Разрешает выводить только тех клиентов и сообщения,
        которые принадлежат пользователю"""
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['clients'].queryset = Client.objects.filter(owner=user)
        self.fields['message'].queryset = MailingMessage.objects.filter(owner=user)

    class Meta:
        model = MailingSettings
        fields = ('end_time', 'sending', 'message', 'setting_status', 'clients',)


class MailingSettingsModeratorForm(StileFormMixin, forms.ModelForm):
    """Форма для модераторов"""
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)

    class Meta:
        model = MailingSettings
        fields = ('setting_status',)


class MailingMessageForm(StileFormMixin, forms.ModelForm):
    """Форма для создания статьи"""
    class Meta:
        model = MailingMessage
        fields = ('title', 'content',)