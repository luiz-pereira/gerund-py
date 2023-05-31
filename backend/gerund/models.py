from django.db import models

# Create your models here.
class Chat(models.Model):
    def _str_(self):
        return self.id

class Message(models.Model):
    content = models.TextField()
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    def _str_(self):
        return self.content

class Person(models.Model):
    name = models.CharField(max_length=30)

    def _str_(self):
        return self.name