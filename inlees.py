import csv, sys
from wijn.models import Appellation, Druif, StreekDruif, StreekWijn

import django
django.setup()

Druif.objects.all().delete()
StreekDruif.objects.all().delete()
StreekWijn.objects.all().delete()
Appellation.objects.all().delete()



for row in csv.DictReader(open("druifjes2.csv")):
    print row
    land = row["Land"].decode("utf-8")
    regio= row["Streek"].decode("utf-8")
    kleur= row["kleur"].decode("utf-8")
    druiven = row["CP"].decode("utf-8")

    druiven = [x.strip() for x in druiven.split(",")]
    for druif in druiven:
        StreekDruif.objects.create(land=land, region=regio, kleur=kleur, druif=druif.lower().strip())
        
for row in csv.DictReader(open("wijnen_nieuw.csv")):
    print row
    land = row["Land"].decode("utf-8")
    regio= row["regio"].decode("utf-8")
    subregio= row["subregio"].decode("utf-8").strip()
    gemeente= row["gemeenten"].decode("utf-8").strip()
    appellation = row["appellations"].decode("utf-8").strip()

    if subregio == "": subregio = None
    if gemeente == "": gemeente = None
    if appellation == "": appellation = None
    
    StreekWijn.objects.create(land=land, region=regio, subregion=subregio, gemeente=gemeente, appellation=appellation)







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

                                             
