import random
from django.contrib.auth.tokens import default_token_generator

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from user.forms import UserRegisterForm, UserForm
from user.models import User
from django.utils.encoding import force_bytes
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetDoneView

from user.services import send_mail_password, send_mail_ready

class IndexView(TemplateView):
    template_name = 'user/index_main.html'
    extra_context = {
        'title': 'Категории'
    }

class LoginView(BaseLoginView):
    template_name = 'user/login.html'

class LogoutView(BaseLogoutView):
    template_name = 'user/logout.html'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('user:login')
    template_name = 'user/register.html'



    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        new_user.save()

        token = default_token_generator.make_token(new_user)
        uid = urlsafe_base64_encode(force_bytes(new_user.pk))
        activation_url = reverse_lazy('user:confirm_email', kwargs={'uidb64': uid, 'token': token})

        current_site = '127.0.0.1:8000'
        send_mail_ready(new_user.email, current_site, activation_url)
        return redirect('user:email_senting')


class UserUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy('user:profile')
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user


# def generate_new_password(request):
#     new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
#     send_mail(
#         subject='Вы сменили пароль',
#         message=f'Ваш пароль: {new_password}!',
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[request.user.email]
#     )
#     request.user.set_password(new_password)
#     request.user.save()
#     return redirect(reverse('catalog:index_main'))


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    request.user.set_password(new_password)
    request.user.save()
    send_mail_password(request.user.email, new_password)
    return redirect(reverse('catalog:index_main'))




class UserConfirmEmailView(View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('user:email_confirmed')
        else:
            return redirect('user:email_info_failed')

class UserConfirmView(TemplateView):
    """ Выводит информацию об успешной регистрации пользователя """
    template_name = 'user/registration_confirmed.html'

class UserConfirmFailView(View):
    """ Выводит информацию о невозможности зарегистрировать пользователя """
    template_name = 'user/email_info_failed.html'


class UserConfirmSentView(PasswordResetDoneView):
    """ Выводит информацию об отправке на почту подтверждения регистрации """
    template_name = "user/registration_sented.html"
