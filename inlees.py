from __future__ import unicode_literals

import csv, sys
from wijn.models import *

import django
django.setup()

DOCG.objects.all().delete()
DOCGDruif.objects.all().delete()
StreekDruif.objects.all().delete()

for row in csv.DictReader(open("docg.csv")):
    for f in row:
        row[f] = None if row[f] == "" else row[f].decode("utf-8")
    print row
    
    land = row["land"]
    regio= row["regio"]
    doc = row["DOC"]
    docg = row["DOCG"]
    kleur = row["kleur"]
    druiven = [row["druif{i}".format(**locals())] for i in range(1,8)]
    
    for (name, isdocg) in [(doc, False), (docg, True)]:
        if name:
            DOCG.objects.create(land=land, regio=regio, name=name, isDOCG=isdocg)
            for i, druif in enumerate(druiven):
                if druif:
                    DOCGDruif.objects.create(land=land, name=name, kleur=kleur, i=i+1, druif=druif)


for row in csv.DictReader(open("druiven_per_land.csv")):
    for f in row:
        row[f] = None if row[f] == "" else row[f].decode("utf-8")
    print row
    
    land = row["land"]
    regio= row["regio"]
    kleur = row["kleur"]
    druiven = [row["druif{i}".format(**locals())] for i in range(1,8)]
    for i, druif in enumerate(druiven):
        if druif:
            StreekDruif.objects.create(land=land, region=regio, kleur=kleur, i=i+1, druif=druif)

import sys; sys.exit()
    
Druif.objects.all().delete()
StreekWijn.objects.all().delete()
Appellation.objects.all().delete()


#for row in csv.DictReader(open("druifjes2.csv")):
#    print row
#    land = row["Land"].decode("utf-8")
#    regio= row["Streek"].decode("utf-8")
#    kleur= row["kleur"].decode("utf-8")
#    druiven = row["CP"].decode("utf-8")#
#
#    druiven = [x.strip() for x in druiven.split(",")]
#    for druif in druiven:
#        StreekDruif.objects.create(land=land, region=regio, kleur=kleur, druif=druif.title().strip())
        
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

                                             
