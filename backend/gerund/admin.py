from django.contrib import admin
from .models import Answer, Question, OutgoingMessage, IncomingEmbedding
# Register your models here.


class OutgoingMessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'type')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'question')

class IncomingEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('content', 'type', 'question')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'answer')

admin.site.register(OutgoingMessage, OutgoingMessageAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(IncomingEmbedding, IncomingEmbeddingAdmin)
admin.site.register(Question, QuestionAdmin)
