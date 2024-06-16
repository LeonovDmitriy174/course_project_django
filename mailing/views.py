import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView, CreateView, TemplateView

from blog.models import BlogPost
from client.models import Client
from mailing.forms import MailingSettingsModeratorForm, MailingSettingsForm, MailingMessageForm
from mailing.models import MailingSettings, MailingMessage, MailingStatus
from mailing.services import get_mailings_from_cache, get_messages_from_cache


class HomeTemplateView(LoginRequiredMixin, TemplateView):
    """Контроллер для главной страницы"""
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        mailing_count = MailingMessage.objects.count()
        is_active_count = MailingSettings.objects.filter(setting_status='Started').count()
        clients_count = Client.objects.distinct('email').count()
        blog_list = list(BlogPost.objects.all())
        random.shuffle(blog_list)
        random_blog_list = blog_list[:3]
        context_data = {
            'mailing_count': mailing_count,
            'is_active': is_active_count,
            'clients_count': clients_count,
            'random_blog_list': random_blog_list,
        }
        return context_data


class MailingMessageCreateView(LoginRequiredMixin, CreateView):
    model = MailingMessage
    fields = ['title', 'content']
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingMessageUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingMessage
    fields = ['title', 'content']
    success_url = reverse_lazy('mailing:list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingMessageForm
        raise PermissionDenied


class MailingMessageDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingMessageForm
        raise PermissionDenied


class MailingMessageListView(LoginRequiredMixin, ListView):
    model = MailingMessage

    def get_queryset(self):
        return get_messages_from_cache()


class MailingMessageDetailView(LoginRequiredMixin, DetailView):
    model = MailingMessage


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:settings_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:settings_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingSettingsForm
        if user.has_perm('mailing.can_change_setting_status'):
            return MailingSettingsModeratorForm
        raise PermissionDenied

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings

    def get_queryset(self):
        return get_mailings_from_cache()


class MailingSettingsDetailView(LoginRequiredMixin, DetailView):
    model = MailingSettings


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:settings_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingSettingsForm
        raise PermissionDenied


class MailingStatusListView(LoginRequiredMixin, ListView):
    model = MailingStatus
