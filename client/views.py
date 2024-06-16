from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from client.forms import ClientForm
from client.models import Client
from client.services import get_clients_from_cache


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        return get_clients_from_cache()


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return ClientForm
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return ClientForm
        raise PermissionDenied
