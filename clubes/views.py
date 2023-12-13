from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, ListView
from registration.models import Tenant
from canchas.models import Field
from canchas.forms import FieldForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


class ClubUpdateView(UpdateView):
    model = Tenant
    template_name = 'clubes/club_settings.html'
    fields = ['clubName', 'clubDescription', 'clubPhoto', 'clubAddress']
    success_url = reverse_lazy('club_settings')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'tenant'):
            try:
                tenant = Tenant.objects.get(username=request.user.username)
            except Tenant.DoesNotExist:
                raise ValueError("Logged in user is not a Tenant")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if hasattr(self.request.user, 'tenant'):
            return self.request.user.tenant
        else:
            raise ValueError("Logged in user is not a Tenant bruh")





class ClubsListView(ListView):
    model = Tenant
    template_name = 'clubes/clubs_list.html'
    context_object_name = 'clubs'


    

class FieldCreateView(CreateView):
    form_class = FieldForm 
    template_name = 'canchas/create_field.html'
    success_url = reverse_lazy('all')

    def form_valid(self, form):
        print("User:", self.request.user)
        print("Tenant:", self.request.user.tenant)
        form.instance.tenant = self.request.user.tenant
        return super().form_valid(form)

def field_detail(request):
    return render(request, 'clubes/club_clientDetailView.html')
