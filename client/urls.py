from django.urls import path
from django.views.decorators.cache import cache_page

from client.apps import ClientConfig
from client.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = ClientConfig.name

urlpatterns = [
    path('list', ClientListView.as_view(), name='list'),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='view'),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name='delete'),
]
