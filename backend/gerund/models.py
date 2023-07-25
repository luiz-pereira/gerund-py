from django.db import models
from pgvector.django import VectorField

# Create your models here.
class OriginalOutgoing(models.Model):
    content = models.TextField()
    type = models.CharField(max_length=30)
    original_incoming = models.ForeignKey('OriginalIncoming', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.id

class OriginalIncoming(models.Model):
    content = models.TextField()
    type = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.id

class OutgoingVariations(models.Model):
    content = models.TextField()
    original_outgoing = models.ForeignKey('OriginalOutgoing', on_delete=models.CASCADE)
    speech_binary = models.BinaryField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.id

class IncomingVariations(models.Model):
    content = models.TextField()
    original_incoming = models.ForeignKey('OriginalIncoming', on_delete=models.CASCADE)
    embedding = VectorField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.id
