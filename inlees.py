import csv, sys
from wijn.models import Appellation, Druif

import django
django.setup()

Druif.objects.all().delete()
Appellation.objects.all().delete()

apps = csv.DictReader(open('appellations.csv'))

for app in apps:
    print app
    regio= app["regio"].decode("latin-1")
    subregio= app["subregio"].decode("latin-1")
    naam = app["appellation"].decode("latin-1")
    wit = app["wit"]
    rood = app["rood"]
    rose =app["rose"]
    mousserend = app["mousserend"]
    zoet = app["zoet"]
    Appellation.objects.create(name=naam, subregion=subregio, region=regio, wit=wit,rood=rood,rose=rose,mousserend=mousserend, zoet=zoet)

druiven = csv.DictReader(open('druifjes.csv'))

for row in druiven:
    print row
    apnaam = row['check'].decode('latin-1')
    ap = Appellation.objects.get(name=apnaam)
    kleur = row['kleur'].decode('latin-1')
    cpdruiven = row['CP'].decode('latin-1').split(",")
    for cpdruif in cpdruiven:
        if not cpdruif.strip(): continue
        Druif.objects.create(appellation=ap, kleur=kleur, cp=True, druif=cpdruif.lower().strip())
    cadruiven = row['CA'].decode('latin-1').split(",")
    for cadruif in cadruiven:
        if not cadruif.strip(): continue
        Druif.objects.create(appellation=ap, kleur=kleur, cp=False, druif=cadruif.lower().strip())

                                             
