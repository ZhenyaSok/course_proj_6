
from django.contrib import admin
from django.urls import path
from client.apps import ClientConfig
from client.views import ClientListView, ClientCreateView, ClientUpdateView, \
    ClientDetailView, ClientDeleteView

app_name = ClientConfig.name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ClientListView.as_view(), name='list'),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('view/<int:pk>/', ClientDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete'),
]
