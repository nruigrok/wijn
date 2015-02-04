import re, random
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from wijn.models import Appellation
from random import shuffle

def index(request):
    return render(request, 'wijn/index.html', locals())


def xxxregio(request):

    ap = Appellation.objects.order_by('?')[0]
    while overlap(ap.name,ap.region):
         ap = Appellation.objects.order_by('?')[0]


    afleiders = list(Appellation.objects.only("region").distinct().values_list("region", flat=True))
    afleiders.remove(ap.region)
    shuffle(afleiders)
    keuzes = afleiders[:3] + [ap.region]
    shuffle(keuzes)
    if request.POST:
        vraag = request.POST["appellation"]
        vraag = Appellation.objects.get(pk=vraag)
        if "region" in request.POST:
            keuze = request.POST["region"]
            goed = (keuze == vraag.region)
        else:
            goed = False
        nvragen = int(request.POST["nvragen"]) + 1
        ngoed = int(request.POST["ngoed"])
        if goed:
            ngoed = ngoed + 1
        perc = 10 + nvragen*90/20
    else:
        nvragen = 0
        ngoed = 0

    return render(request, 'wijn/regio.html', locals())


def regio(request):

    vraagtype = random.choice(["welkeregio", "welkeap"])

    ap = Appellation.objects.order_by('?')[0]
    while overlap(ap.name,ap.region):
         ap = Appellation.objects.order_by('?')[0]

    if vraagtype == "welkeap":
        vraagtekst = "Welke appellation ligt in {ap.region}".format(**locals())

        afleiders = list(Appellation.objects.exclude(region=ap.region))
        shuffle(afleiders)
        keuzes = afleiders[:3] + [ap]
        keuzes = [(k.id, k.name) for k in keuzes]
    elif vraagtype == "welkeregio":
        vraagtekst = u"In welke regio ligt {ap.name}".format(**locals())
        afleiders = list(Appellation.objects.only("region").distinct().values_list("region", flat=True))
        afleiders.remove(ap.region)
        shuffle(afleiders)
        keuzes = afleiders[:3] + [ap.region]
        keuzes = [(region, region) for region in keuzes]

    shuffle(keuzes)

    if request.POST:
        oudevraag = request.POST["vraagtekst"]
        vraag = request.POST["vraag"]
        oudevraagtype = request.POST["vraagtype"]
        antwoord = request.POST["antwoord"]
        vraag = Appellation.objects.get(pk=vraag)


        if oudevraagtype == "welkeap":
            antwoord = Appellation.objects.get(pk=antwoord)
        elif oudevraagtype == "welkeregio":
            vraag = vraag.region

        goed = (antwoord == vraag)

        nvragen = int(request.POST["nvragen"]) + 1
        ngoed = int(request.POST["ngoed"])
        if goed:
            ngoed = ngoed + 1
        perc = 10 + nvragen*90/20
    else:
        nvragen = 0
        ngoed = 0

    return render(request, 'wijn/regio.html', locals())

def regiokiezer(request):
    regiolijst = list(Appellation.objects.only("region").exclude(region="").exclude(subregion="").distinct().values_list("region", flat=True))
    return render(request, 'wijn/regiokiezer.html', locals())

def kleurperregio(request):
    regiolijst = list(Appellation.objects.only("region").exclude(region="").distinct().values_list("region", flat=True))
    return render(request, 'wijn/kleurperregio.html', locals())


def overlap(a,b):
    child = re.split("\W", a.lower())
    parent = re.split("\W", b.lower())
    for word in child:
        if word in parent:
            return True

def subregio(request, regio):
    appellations = Appellation.objects.exclude(subregion="")
    if regio != "all":
        appellations = appellations.filter(region=regio)

    ap = appellations.order_by('?')[0]
    while overlap(ap.name,ap.subregion):
         ap = appellations.order_by('?')[0]


    afleiders = list(appellations.filter(region=ap.region).only("subregion").distinct().values_list("subregion", flat=True))
    afleiders.remove(ap.subregion)
    shuffle(afleiders)
    keuzes = afleiders[:3] + [ap.subregion]
    shuffle(keuzes)
    if request.POST:
        vraag = request.POST["appellation"]
        vraag = Appellation.objects.get(pk=vraag)
        if "subregion" in request.POST:
            keuze = request.POST["subregion"]
            goed = (keuze == vraag.subregion)
        else:
            goed = False
        nvragen = int(request.POST["nvragen"]) + 1
        ngoed = int(request.POST["ngoed"])
        if goed:
            ngoed = ngoed + 1
        perc = 10 + nvragen*90/20
    else:
        nvragen = 0
        ngoed = 0

    return render(request, 'wijn/subregio.html', locals())


def kleur(request, regio):
    appellations = Appellation.objects.only("region").distinct()
    if regio !="all":
        appellations = appellations.filter(region=regio)

    ap = appellations.order_by('?')[0]

    if request.POST:
        vraag = request.POST["appellation"]
        vraag = Appellation.objects.get(pk=vraag)
        goedeantwoord = ", ".join([a for a in ["rood", "wit", "rose", "mousserend", "zoet"] if getattr(vraag, a)]).title()
        keuze = ", ".join([a for a in ["rood", "wit", "rose", "mousserend", "zoet"] if a in request.POST]).title()
        goed = keuze == goedeantwoord
        nvragen = int(request.POST["nvragen"]) + 1
        ngoed = int(request.POST["ngoed"])
        if goed:
            ngoed = ngoed + 1
        perc = 10 + nvragen*90/20

    else:
        nvragen = 0
        ngoed = 0

    return render(request, 'wijn/kleur.html', locals())


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = UserCreationForm.Meta.model
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)

            return HttpResponseRedirect("/wijn/")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
