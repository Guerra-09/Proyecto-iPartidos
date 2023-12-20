from django.contrib import admin
from .models import Tenant, Client, FieldRentHistory, ReservationHistory


class TenantAdmin(admin.ModelAdmin):
    ...

class ClientAdmin(admin.ModelAdmin):
    ...

class FieldRentHistoryAdmin(admin.ModelAdmin):
    pass

class ReservationHistoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tenant, TenantAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(FieldRentHistory, FieldRentHistoryAdmin)
admin.site.register(ReservationHistory, ReservationHistoryAdmin)
