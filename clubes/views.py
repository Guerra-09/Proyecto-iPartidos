from django.shortcuts import render
from django.views.generic import UpdateView
from registration.models import Tenant
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class ClubUpdateView(UpdateView):
    model = Tenant
    template_name = 'clubes/club_settings.html'
    fields = ['clubName', 'clubDescription', 'clubPhoto', 'clubAddress']
    success_url = '/clubes/all'

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

def fetchClubs(request):
    return render(request, 'clubes/home.html')