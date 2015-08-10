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


class Druif(models.Model):
    appellation = models.ForeignKey(Appellation)
    kleur = models.CharField(max_length=255)
    cp =  models.BooleanField(default=True)
    druif = models.CharField(max_length=255)



class StreekWijn(models.Model):
    land = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    subregion = models.CharField(max_length=255, null = True)
    gemeente = models.CharField(max_length=255, null = True)
    appellation = models.CharField(max_length=255, null = True)
    
class StreekDruif(models.Model):
    land = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    kleur = models.CharField(max_length=255)
    druif = models.CharField(max_length=255)

class DOCG(models.Model):
    land = models.CharField(max_length=255)
    regio = models.CharField(max_length=255)
    subregio = models.CharField(max_length=255, null = True)
    name = models.CharField(max_length=255)
    isDOCG = models.BooleanField()

class DOCGDruif(models.Model):
    land = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    druif = models.CharField(max_length=255)
