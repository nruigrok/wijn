from django.contrib.auth.models import User
from django.db import models

class Appellation(models.Model):
    name = models.CharField(max_length=255)
    subregion = models.CharField(max_length=255, null = True)
    region = models.CharField(max_length=255)
    wit = models.BooleanField(default=False)
    rood = models.BooleanField(default=False)
    rose = models.BooleanField(default=False)
    mousserend = models.BooleanField(default=False)
    zoet = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Score(models.Model):
    vraag = models.CharField(max_length=255)
    region = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
