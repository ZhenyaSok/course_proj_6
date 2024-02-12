from django.urls import path
from django.conf.urls.static import static
from config import settings
from user.apps import UserConfig
from user.views import LoginView, LogoutView, RegisterView, UserUpdateView, generate_new_password, \
    UserConfirmEmailView, UserConfirmView, UserConfirmFailView, UserConfirmSentView, IndexView

app_name = UserConfig.name




urlpatterns = [
    path('', IndexView.as_view(), name='index_main'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),

    path('confirm_email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email_confirmed/', UserConfirmView.as_view(), name='email_confirmed'),
    path('email_info_failed/', UserConfirmFailView.as_view(), name='email_info_failed'),
    path('email_senting/', UserConfirmSentView.as_view(), name='email_senting'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)