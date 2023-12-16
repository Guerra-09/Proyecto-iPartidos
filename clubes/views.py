from django.shortcuts import render
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from registration.models import Tenant
from canchas.models import Field
from clubes.forms import ClubForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.db.models import Q

#   
class ClubUpdateView(UpdateView):
    model = Tenant
    template_name = 'clubes/club_settings.html'
    form_class = ClubForm
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

#   
class ClubsListView(ListView):
    model = Tenant
    template_name = 'clubes/clubs_list.html'
    context_object_name = 'clubs'

#   
def field_detail(request):
    return render(request, 'clubes/club_clientDetailView.html')

#   
class ClubClientDetailView(DetailView):
    model = Tenant
    template_name = 'clubes/club_clientDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        players_per_side = self.request.GET.get('players_per_side')
        ground_type = self.request.GET.get('ground_type')

        filters = Q(tenant=self.object)
        if players_per_side:
            filters &= Q(playersPerSide=players_per_side)
        if ground_type:
            filters &= Q(groundType=ground_type)

        context['fields'] = Field.objects.filter(filters)
        context['club'] = self.object.tenant

        context['GROUND_CHOICES'] = Field.GROUND_CHOICES
        

        return context
    
