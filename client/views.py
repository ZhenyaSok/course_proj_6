from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from client.forms import ClientForm
from client.models import Client


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter()
        return queryset

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm


class ClientUpdateView(UpdateView):
    model = Client

class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client