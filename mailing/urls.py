from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import MailingMessageListView, MailingMessageCreateView, MailingMessageDetailView, \
    MailingMessageUpdateView, MailingMessageDeleteView, MailingSettingsListView, MailingSettingsCreateView, \
    MailingSettingsDetailView, MailingSettingsUpdateView, MailingSettingsDeleteView, HomeTemplateView, \
    MailingStatusListView, MailingStatusDetailView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('list', MailingMessageListView.as_view(), name='list'),
    path('create/', MailingMessageCreateView.as_view(), name='create'),
    path('<int:pk>/', cache_page(60)(MailingMessageDetailView.as_view()), name='view'),
    path('<int:pk>/update/', MailingMessageUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', MailingMessageDeleteView.as_view(), name='delete'),
    path('settings/', MailingSettingsListView.as_view(), name='settings_list'),
    path('settings/create/', MailingSettingsCreateView.as_view(), name='settings_create'),
    path('settings/<int:pk>/', cache_page(60)(MailingSettingsDetailView.as_view()), name='settings_view'),
    path('settings/<int:pk>/update/', MailingSettingsUpdateView.as_view(), name='settings_edit'),
    path('settings/<int:pk>/delete/', MailingSettingsDeleteView.as_view(), name='settings_delete'),
    path('status_list', MailingStatusListView.as_view(), name='mailing_status_list'),
    path('status_detail/<int:pk>', MailingStatusDetailView.as_view(), name='mailing_status_detail'),
]