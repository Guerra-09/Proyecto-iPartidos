from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Field
from registration.models import FieldRentHistory, ReservationHistory
from .forms import FieldForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import MultipleObjectsReturned
from copy import copy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from reservation.models import Reservation


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


def clients_reservations(request):
    rent_histories = FieldRentHistory.objects.filter(reservation__field__tenant=request.user.tenant).order_by('-id')
    print(rent_histories)
    return render(request, 'canchas/clients_reservations.html', {'reservations': rent_histories})


def delete_client_reservation(request, reservation_id):
    rent_history = get_object_or_404(FieldRentHistory, reservation_id=reservation_id)
    user = rent_history.takenBy
    reservation_histories = ReservationHistory.objects.filter(client=user, field=rent_history.reservation.field, dateToReservate=rent_history.reservation.dateToReservate)
    reservation_histories.update(status='cancelled')


    


    return render(request, 'canchas/client_reservation_deleted_successfully.html')
    