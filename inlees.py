import csv, sys
from wijn.models import Appellation

import django
django.setup()

Appellation.objects.all().delete()

apps = csv.DictReader(sys.stdin)

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

