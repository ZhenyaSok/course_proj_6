from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from client_service.forms import MessageForm
from client_service.models import MessageMailing


class MessageListView(ListView):
    model = MessageMailing

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(category_id=self.kwargs.get('pk'))
    #     return queryset
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:  # для работников и суперпользователя
            queryset = super().get_queryset()
        else:  # для остальных пользователей
            queryset = super().get_queryset().filter(owner=user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список Сообщений'
        return context_data




class MessageCreateView(CreateView):
    model = MessageMailing
    form_class = MessageForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user:list', args=[self.object.category.pk])



class MessageUpdateView(UpdateView):
    model = MessageMailing
    form_class = MessageForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user:list', args=[self.object.category.pk])

class MessageDetailView(DetailView):
    model = MessageMailing

    def get_object(self, queryset=None, **kwargs):
        self.object = super().get_object(queryset)

        return self.object

class MessageDeleteView(DeleteView):
    model = MessageMailing
    success_url = reverse_lazy('user:list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        return self.object


