from django.urls import path
from client_service.apps import ClientServiceConfig
from client_service.views import MessageListView, MessageCreateView, MessageUpdateView, MessageDetailView, \
    MessageDeleteView, SettingMailingDetailView, SettingMailingListView, SettingMailingUpdateView, \
    SettingMailingCreateView, SettingMailingDeleteView, LogsDeleteView, LogsDetailView, LogsListView, toggle_active

app_name = ClientServiceConfig.name

urlpatterns = [
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),



    path('list/', SettingMailingListView.as_view(), name='list'),
    path('toggle-active/<int:pk>/', toggle_active, name='toggle_active'),
    path('view/<int:pk>/', SettingMailingDetailView.as_view(), name='view'),
    path('create/', SettingMailingCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', SettingMailingUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', SettingMailingDeleteView.as_view(), name='delete'),

    path('logs', LogsListView.as_view(), name='log_list'),
    path('log/<int:pk>/', LogsDetailView.as_view(), name='log_detail'),
    path('log_delete/<int:pk>/', LogsDeleteView.as_view(), name='log_delete'),
]