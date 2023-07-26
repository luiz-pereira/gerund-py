from django.contrib import admin
from .models import Answer, Question, OutgoingMessages, IncomingEmbeddings
# Register your models here.


class OutgoingMessagesAdmin(admin.ModelAdmin):
    list_display = ('content', 'type')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'question')

class IncomingEmbeddingsAdmin(admin.ModelAdmin):
    list_display = ('content', 'type', 'question')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'answer')

admin.site.register(OutgoingMessages, OutgoingMessagesAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(IncomingEmbeddings, IncomingEmbeddingsAdmin)
admin.site.register(Question, QuestionAdmin)
