from django.contrib import admin
from .models import OriginalOutgoing, OriginalIncoming, OutgoingVariations, IncomingVariations
# Register your models here.


class OutgoingVariationsAdmin(admin.ModelAdmin):
    list_display = ('content', 'original_outgoing')

class OriginalOutgoingAdmin(admin.ModelAdmin):
    list_display = ('content', 'type', 'original_incoming')

class IncomingVariationsAdmin(admin.ModelAdmin):
    list_display = ('content', 'original_incoming')

class OriginalIncomingAdmin(admin.ModelAdmin):
    list_display = ('content', 'type')

admin.site.register(OutgoingVariations, OutgoingVariationsAdmin)
admin.site.register(OriginalOutgoing, OriginalOutgoingAdmin)
admin.site.register(IncomingVariations, IncomingVariationsAdmin)
admin.site.register(OriginalIncoming, OriginalIncomingAdmin)
