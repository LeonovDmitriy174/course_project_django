from django.core.cache import cache

from client.models import Client
from config.settings import CACHE_ENABLED


def get_clients_from_cache():
    """Получает список клиентов из кэша, если он пустой получает из базы данных"""
    if not CACHE_ENABLED:
        return Client.objects.all()
    key = 'client_list'
    clients = cache.get(key)
    if clients is not None:
        return clients
    clients = Client.objects.all()
    cache.set(key, clients)
    return clients
