import calendar
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from client_service.forms import MessageForm, SettingMailingForm
from client_service.models import MessageMailing, SettingMailing, Logs


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


class SettingMailingCreateView(LoginRequiredMixin, CreateView):
    model = SettingMailing
    form_class = SettingMailingForm
    extra_context = {
        'title': 'Создание'
    }

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def form_valid(self, form):
        current_time = timezone.localtime(timezone.now())
        new_mailing = form.save()
        new_mailing.save()
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        if form.is_valid():
            recipients = form.cleaned_data['recipients']
            new_mailing = form.save()
            if new_mailing.start_time > current_time:
                new_mailing.next_send = new_mailing.start_time
            else:
                if new_mailing.periodicity == "Раз в день":
                    new_mailing.next_send = new_mailing.start_time + timedelta(days=1)

                if new_mailing.periodicity == "Раз в неделю":
                    new_mailing.next_send = new_mailing.start_time + timedelta(days=7)

                if new_mailing.periodicity == "Раз в месяц":
                    today = datetime.today()
                    days = calendar.monthrange(today.year, today.month)[1]
                    new_mailing.next_send = current_time + timedelta(days=days)

                for client in recipients:
                    new_mailing.recipients.add(client.pk)
                new_mailing.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('client_service:list')




class SettingMailingUpdateView(LoginRequiredMixin, UpdateView):
    model = SettingMailing
    form_class = SettingMailingForm
    extra_context = {
        'title': 'Редактирование'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            if self.object.owner != self.request.user or self.request.user.filter(groups__name='manager').exists():
                raise Http404
        return self.object

    def get_initial(self):
        initial = super().get_initial()
        initial['owner'] = self.request.user
        return initial

    def form_valid(self, form):
        current_time = timezone.localtime(timezone.now())
        new_mailing = form.save()
        new_mailing.save()
        self.object = form.save()
        self.object.save()
        if form.is_valid():
            recipients = form.cleaned_data['recipients']
            new_mailing = form.save()
            if new_mailing.start_time > current_time:
                new_mailing.next_send = new_mailing.start_time
            else:
                if new_mailing.periodicity == "Раз в день":
                    new_mailing.next_send = new_mailing.start_time + timedelta(days=1)

                if new_mailing.periodicity == "Раз в неделю":
                    new_mailing.next_send = new_mailing.start_time + timedelta(days=7)

                if new_mailing.periodicity == "Раз в месяц":
                    today = datetime.today()
                    days = calendar.monthrange(today.year, today.month)[1]
                    new_mailing.next_send = new_mailing.start_time + timedelta(days=days)

                for client in recipients:
                    new_mailing.recipients.add(client.pk)
                new_mailing.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('client_service:view', args=[self.object.pk])


class SettingMailingListView(LoginRequiredMixin, ListView):
    model = SettingMailing

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:  # для работников и суперпользователя
            queryset = super().get_queryset()
        else:  # для остальных пользователей
            queryset = super().get_queryset().filter(owner=user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список рассылок'

        context_data['all'] = context_data['object_list'].count()
        context_data['active'] = context_data['object_list'].filter(status=SettingMailing.STARTED).count()
        context_data['completed'] = context_data['object_list'].filter(status=SettingMailing.COMPLETED).count()

        return context_data


def toggle_active(request, pk):
    if request.user.is_staff:
        client_service = SettingMailing.objects.get(pk=pk)
        client_service.is_active = not client_service.is_active
        client_service.save()
        return redirect('client_service:list')


class SettingMailingDetailView(LoginRequiredMixin, DetailView):
    model = SettingMailing

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Детали рассылки:'
        return context_data


class SettingMailingDeleteView(LoginRequiredMixin, DeleteView):
    model = SettingMailing

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            if self.object.owner != self.request.user or self.request.user.filter(groups__name='manager').exists():
                raise Http404
        return self.object

    def get_success_url(self):
        return reverse('client_service:list')


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:  # для работников и суперпользователя
            queryset = super().get_queryset()
        else:  # для остальных пользователей
            queryset = super().get_queryset().filter(owner=user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = 'Список логов'

        context_data['all'] = context_data['object_list'].count()
        context_data['success'] = context_data['object_list'].filter(status=True).count()
        context_data['error'] = context_data['object_list'].filter(status=False).count()

        return context_data


class LogsDetailView(LoginRequiredMixin, DetailView):
    model = Logs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        log = self.get_object()
        context_data['title'] = f'log: {log.pk}'
        return context_data


class LogsDeleteView(LoginRequiredMixin, DeleteView):
    model = Logs
    success_url = reverse_lazy('client_service:log_list')
    extra_context = {
        'title': 'Delete Log'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.is_superuser:
            if self.object.owner != self.request.user or self.request.user.filter(groups__name='manager').exists():
                raise Http404
        return self.object

