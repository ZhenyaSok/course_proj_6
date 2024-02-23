from django.http import Http404
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from materials.models import Material
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from .forms import MaterialForm
from .func_send import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    success_url = reverse_lazy('materials:list')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_mat = form.save()
    #         new_mat.slug = slugify(new_mat.title)
    #         new_mat.save()
    #
    #     return super().form_valid(form)

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('materials:list')

class MaterialListView(ListView):
    model = Material

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset



class MaterialDetailView(DetailView):
    model = Material

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        if self.object.views_count == 100:
            send_mail()
        return self.object



class MaterialUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    success_url = reverse_lazy('materials:list')
    permission_required = ['materials.change_material']
    # success_url = reverse_lazy('materials:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)



    def get_success_url(self):
        return reverse('materials:view', args=[self.kwargs.get('pk')])

class MaterialDeleteView(PermissionRequiredMixin, DeleteView):
    model = Material
    success_url = reverse_lazy('materials:list')
    permission_required = ['materials.change_material']



class UserConfirmFailView(View):
    """ Выводит информацию об успешной регистрации пользователя """
    template_name = 'materials/not_delete_confirmed.html'