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

