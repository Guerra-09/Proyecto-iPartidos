from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Field
from .forms import FieldForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import MultipleObjectsReturned
from copy import copy


class FieldListView(ListView):
    model = Field
    template_name = 'canchas/userFields_list.html'
    context_object_name = 'fields'

    def get_queryset(self):
        return Field.objects.filter(tenant=self.request.user.tenant)


class FieldCreateView(CreateView):
    form_class = FieldForm 
    template_name = 'canchas/create_field.html'
    success_url = reverse_lazy('all')

    def form_valid(self, form):
        print("User:", self.request.user)
        print("Tenant:", self.request.user.tenant)
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)


class FieldUpdateView(LoginRequiredMixin, UpdateView):
    model = Field
    form_class = FieldForm
    template_name = 'canchas/create_field.html'
    success_url = reverse_lazy('canchas_list')

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

    def get_object(self, queryset=None):
        """Obtener el objeto Field del Tenant actualmente autenticado."""
        if queryset is None:
            queryset = self.get_queryset()
        # Get the 'pk' from the URL
        pk = self.kwargs.get('pk')
        # Get the object with the given 'pk'
        obj = get_object_or_404(queryset, pk=pk)
        return obj


class FieldDetailView(DetailView):
    model = Field
    template_name = 'canchas/fields_detail.html'
    context_object_name = 'cancha'


