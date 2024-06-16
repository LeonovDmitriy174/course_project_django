from django import forms

from client.models import Client
from users.forms import StileFormMixin


class ClientForm(StileFormMixin, forms.ModelForm):
    """Форма для создания статьи"""
    class Meta:
        model = Client
        fields = ('email', 'name', 'comment',)
