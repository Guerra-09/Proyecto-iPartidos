from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Field


class FieldListView(ListView):
    model = Field
    template_name = 'canchas/fields_list.html'
    context_object_name = 'fields'


class FieldDetailView(DetailView):
    model = Field
    template_name = 'canchas/fields_detail.html'
    context_object_name = 'cancha'

