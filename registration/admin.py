from django.contrib import admin
from .models import Tenant, Client, FieldRentHistory


class TenantAdmin(admin.ModelAdmin):
    ...

class ClientAdmin(admin.ModelAdmin):
    ...

admin.site.register(Tenant, TenantAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(FieldRentHistory)