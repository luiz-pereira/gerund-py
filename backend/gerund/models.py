from django.db import models
from pgvector.django import VectorField

# Create your models here.
class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.id

class Question(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    script = models.ForeignKey('Script', on_delete=models.CASCADE)

    def _str_(self):
        return self.id

class OutgoingMessage(models.Model):
    content = models.TextField()
    type = models.CharField(max_length=36)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, null=True)
    speech_binary = models.BinaryField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.id

class IncomingEmbedding(models.Model):
    content = models.TextField()
    type = models.CharField(max_length=36)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=True)
    embedding = VectorField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.id

class Script(models.Model):
    custom_prompt = models.TextField()
    presentation = models.TextField()
    new_product = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.id
