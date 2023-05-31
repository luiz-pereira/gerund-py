from django.contrib import admin
from .models import Chat, Message, Person

# Register your models here.

class ChatAdmin(admin.ModelAdmin):
    list_display = ('message_set',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'chat', 'person')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'message_set')

# Register your models here.

admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Person, PersonAdmin)
