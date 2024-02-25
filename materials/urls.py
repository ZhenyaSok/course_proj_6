from django.urls import path
from materials.apps import MaterialsConfig
from materials.views import MaterialCreateView, MaterialListView, MaterialDetailView, MaterialUpdateView, \
    MaterialDeleteView, HomeView

app_name = MaterialsConfig.name


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('create/', MaterialCreateView.as_view(), name='product_create'),
    path('', MaterialListView.as_view(), name='list'),
    path('view/<int:pk>', MaterialDetailView.as_view(), name='view'),
    path('edit/<int:pk>', MaterialUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', MaterialDeleteView.as_view(), name='delete'),


]
