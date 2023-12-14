from django.contrib import admin
from .models import Tenant, Client


class TenantAdmin(admin.ModelAdmin):
    ...

class ClientAdmin(admin.ModelAdmin):
    ...

admin.site.register(Tenant, TenantAdmin)
admin.site.register(Client, ClientAdmin)