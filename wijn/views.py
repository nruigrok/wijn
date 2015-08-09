import re, random
# Create your views here.

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from wijn.models import Appellation, Score, Druif, StreekWijn, StreekDruif
from random import shuffle

def index(request):
    return render(request, 'wijn/index.html', locals())


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

        if nvragen == 20:
            user = request.user if request.user.is_authenticated() else None
            Score.objects.create(vraag='regio', user=user, score=ngoed)

    else:
        nvragen = 0
        ngoed = 0

    return render(request, 'wijn/regio.html', locals())



def kleurmeerkeuze(request, regio='all'):
    vraagtype = random.choice(["welkekleur", "welkeap"])
    intext = '' if regio == 'all' else ' in {regio}'.format(**locals())

    appellations = Appellation.objects.exclude(rood=False,wit=False,rose=False,zoet=False,mousserend=False)
    if regio != 'all':
        appellations = appellations.filter(region=regio)
    ap = appellations.order_by('?')[0]
    apkleur = kleurstring(ap)

    if vraagtype == "welkekleur":
        vraagtekst = u"Welke kleur mag{intext} in {ap.name}".format(**locals())
        keuzes = [apkleur]
        afleiders = list(appellations.order_by('?'))
        for afleider in afleiders:
            if kleurstring(afleider) not in keuzes:
                keuzes.append(kleurstring(afleider))
        keuzes = keuzes[:4]
        keuzes = [(k, k) for k in keuzes]
    else:
        vraagtekst = u"Welke appellation{intext} mag {apkleur}".format(**locals())
        keuzes = [ap]
        afleiders = list(appellations.order_by('?'))
        for afleider in afleiders:
            if kleurstring(afleider) != apkleur:
                keuzes.append(afleider)
        keuzes = keuzes[:4]
        keuzes = [(k.id, k.name) for k in keuzes]

    shuffle(keuzes)

    if request.POST:
        oudevraag = request.POST["vraagtekst"]
        vraag = request.POST["vraag"]
        oudevraagtype = request.POST["vraagtype"]
        antwoord = request.POST["antwoord"]
        vraag = Appellation.objects.get(pk=vraag)


        if oudevraagtype == "welkekleur":
            goedeantwoord = kleurstring(vraag)
            goed = (antwoord == goedeantwoord)
        elif oudevraagtype == "welkeap":
            goedeantwoord = vraag.name
            antwoord = Appellation.objects.get(pk=antwoord)
            goed = (antwoord.name == goedeantwoord)
            antwoordkleuren = kleurstring(antwoord)
            antwoord = "{antwoord} ({antwoordkleuren})".format(**locals())

        nvragen = int(request.POST["nvragen"]) + 1
        ngoed = int(request.POST["ngoed"])
        if goed:
            ngoed = ngoed + 1
        perc = 10 + nvragen*90/20

        if nvragen == 20:
            user = request.user if request.user.is_authenticated() else None
            Score.objects.create(vraag='kleurmeerkeuze', user=user, score=ngoed)

    else:
        nvragen = 0
        ngoed = 0

    return render(request, 'wijn/kleurmeerkeuze.html', locals())


def druiven(request, regio='all'):
    vraagtype = random.choice(["welkedruif","apdruif"])
    appellations = Appellation.objects.exclude(rood=False,wit=False,rose=False,zoet=False,mousserend=False)
    if regio != 'all':
        appellations = appellations.filter(region=regio)
    apps = appellations.order_by('?')

    intext = '' if regio == 'all' else ' in {regio}'.format(**locals())

    ap = appellations.order_by('?')[0]
    while not ap.druif_set.exists():
        ap = appellations.order_by('?')[0]


    if vraagtype == "welkedruif":
        druiven = list(ap.druif_set.filter(cp=True))
        shuffle(druiven)
        apdruif = druiven[0]
        vraagkleur = apdruif.kleur
        vraagtekst = u"Welke druif mag {intext} gebruikt worden in {ap.name} ({vraagkleur})".format(**locals())
        keuzes = [apdruif]
        afleiders = []
        for app in apps:
            appdruiven =list(app.druif_set.filter(cp=True, kleur=apdruif.kleur))
            for druif in appdruiven:
                afleiders.append(druif)
        for afleider in afleiders:
            if afleider.druif not in [d.druif for d in druiven]:
                if afleider.druif not in [k.druif for k in keuzes]:
                    keuzes.append(afleider)
        keuzes = keuzes[:4]
        keuzes = [(k.id, k.druif) for k in keuzes]
    else:
        druiven = list(ap.druif_set.filter(cp=True))
        shuffle(druiven)
        apdruif = druiven[0]
        vraagkleur = apdruif.kleur
        vraagtekst = u"Welke appellation {intext} mag {apdruif.druif} gebruiken ({vraagkleur})".format(**locals())
        keuzes = [ap]
        for afleider in apps:
            if apdruif.druif not in [d.druif for d in afleider.druif_set.all()]:
                if afleider.druif_set.exists(): # geen afleiders waarvan we de druiven niet weten
                    keuzes.append(afleider)
        keuzes = keuzes[:4]
        keuzes = [(k.id, k.name) for k in keuzes]

    shuffle(keuzes)

    if request.POST:
        oudevraag = request.POST["vraagtekst"]
        vraag = request.POST["vraag"]
        oudevraagtype = request.POST["vraagtype"]
        antwoord = request.POST["antwoord"]
        vraagkleur = request.POST["vraagkleur"]
        vraag = Appellation.objects.get(pk=vraag)

        if oudevraagtype == "welkedruif":
            antwoord = Druif.objects.get(pk=antwoord).druif
            antwoorden = [d.druif for d in vraag.druif_set.filter(kleur=vraagkleur, cp=True)]
            goed = antwoord in antwoorden
            goedeantwoord = ",".join(antwoorden)
        elif oudevraagtype == "apdruif":
            goedeantwoord = vraag
            antwoord = Appellation.objects.get(pk=antwoord)
            goed = (antwoord == goedeantwoord)
            goededruiven =  ",".join(d.druif for d in vraag.druif_set.filter(kleur=vraagkleur, cp=True))
            goedeantwoord = u"{goedeantwoord.name} ({goededruiven})".format(**locals())
            antwoorddruiven =  ",".join(d.druif for d in antwoord.druif_set.filter(kleur=vraagkleur, cp=True))
            if not antwoorddruiven:
                antwoorddruiven = "maakt geen {vraagkleur}".format(**locals())
            antwoord = u"{antwoord.name} ({antwoorddruiven})".format(**locals())

        nvragen = int(request.POST["nvragen"]) + 1
        ngoed = int(request.POST["ngoed"])
        if goed:
            ngoed = ngoed + 1
        perc = 10 + nvragen*90/20

        if nvragen == 20:
            user = request.user if request.user.is_authenticated() else None
            Score.objects.create(vraag='welkedruif', user=user, score=ngoed)

    else:
        nvragen = 0
        ngoed = 0

    return render(request, 'wijn/druiven.html', locals())


def streekdruiven(request, land='all'):
    vraagtype = random.choice(["welkedruif","apdruif"])
    vraagtype = "welkedruif"
    streekdruiven = StreekDruif.objects.all()
    if land != 'all':
        streekdruiven = streekdruiven.filter(land=land)

    intext = '' if regio == 'all' else ' in {land}'.format(**locals())

    streekdruif = streekdruiven.order_by('?')[0]
    vraagkleur = streekdruif.kleur

    if vraagtype == "welkedruif":
        vraagtekst = u"Welke druif mag {intext} gebruikt worden in {streekdruif.region} ({streekdruif.kleur})".format(**locals())
        keuze = streekdruif.druif
        alternatieven = list(streekdruiven.filter(region=streekdruif.region).values_list("druif", flat=True))        
        afleiders = list(set(streekdruiven.filter(kleur=streekdruif.kleur).exclude(druif__in=alternatieven).values_list("druif", flat=True)))
    else:
        vraagtekst = u"Welke regio {intext} mag {streekdruif.druif} gebruiken ({streekdruif.kleur})".format(**locals())
        keuze = streekdruif.region
        alternatieven = list(streekdruiven.filter(druif=streekdruif.druif).values_list("region", flat=True))
        afleiders = list(set(streekdruiven.exclude(region__in=alternatieven).values_list("region", flat=True)))

    shuffle(afleiders)
    keuzes = [keuze] + afleiders[:3]
    shuffle(keuzes)

    if request.POST:
        oudevraag = request.POST["vraagtekst"]
        vraag = StreekDruif.objects.get(pk=request.POST["vraag"])        
        oudevraagtype = request.POST["vraagtype"]
        antwoord = request.POST["antwoord"]

        vraagdruiven = [d.druif for d in StreekDruif.objects.filter(region=vraag.region, kleur=vraag.kleur)]
        
        if oudevraagtype == "welkedruif":
            goed = antwoord in vraagdruiven
            goedeantwoord = ",".join(vraagdruiven)
        elif oudevraagtype == "apdruif":
            goed = (antwoord == vraag.region)
            goededruiven = ",".join(vraagdruiven)
            goedeantwoord = u"{vraag.region} ({goededruiven})".format(**locals())
            
            antwoorddruiven =  ",".join(d.druif for d in streekdruiven.filter(region=antwoord, kleur=vraag.kleur))
            if not antwoorddruiven:
                antwoorddruiven = "maakt geen {vraag.kleur}".format(**locals())
            antwoord = u"{antwoord} ({antwoorddruiven})".format(**locals())

        nvragen = int(request.POST["nvragen"]) + 1
        ngoed = int(request.POST["ngoed"])
        if goed:
            ngoed = ngoed + 1
        perc = 10 + nvragen*90/20

        if nvragen == 20:
            user = request.user if request.user.is_authenticated() else None
            Score.objects.create(vraag='welkedruif', user=user, score=ngoed)
    else:
        nvragen = 0
        ngoed = 0

    return render(request, 'wijn/streekdruiven.html', locals())




def regiokiezer(request, next):
    regiolijst = Appellation.objects.only("region").exclude(region="")
    if next == 'subregio':
        regiolijst = regiolijst.exclude(subregion="")
    regiolijst = list(regiolijst.distinct().values_list("region", flat=True))
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


        if nvragen == 20:
            user = request.user if request.user.is_authenticated() else None
            Score.objects.create(vraag='Subregio', region=regio, user=user, score=ngoed)
    else:
        nvragen = 0
        ngoed = 0

    return render(request, 'wijn/subregio.html', locals())



def landenkiezer(request, next):
    if next == "subregios2":
        landenlijst = StreekWijn.objects.exclude(subregion__isnull=True)
    elif next == "gemeentes":
        landenlijst = StreekWijn.objects.exclude(gemeente__isnull=True)
    elif next == "appellations":
        landenlijst = StreekWijn.objects.exclude(appellation__isnull=True)
    elif next == "streekdruiven":
        landenlijst = StreekDruif.objects.all()
    landenlijst = list(landenlijst.only("land").distinct().values_list("land", flat=True))
    return render(request, 'wijn/landenkiezer.html', locals())


from django.views.generic import FormView
from django import forms

class ChoiceView(FormView):
    template_name = "wijn/choice.html"
    class form_class(forms.Form):
        vraag = forms.HiddenInput()
        nvragen = forms.HiddenInput()
        ngoed = forms.HiddenInput()
        antwoord = forms.TextInput()

    def get_context_data(self, **kwargs):
        objects = self.get_objects()
        if 'land' in self.kwargs:
            objects = objects.filter(land=self.kwargs['land'])
        goed = self.get_goed(objects)
        afleiders = list(self.get_afleiders(objects, goed))
        shuffle(afleiders)
        opties = [self.optie_text(goed)] + afleiders[:3]
        shuffle(opties)
        vraagtext = self.get_vraag(goed)
        nvragen = ngoed = 0
        kwargs.update(locals())
        return kwargs

    def form_valid(self, form):
        oudegoed = self.get_objects().get(pk=form.data['goed'])
        antwoord = form.data['antwoord']
        oudevraag = self.get_vraag(oudegoed)
        goedeantwoord = self.optie_text(oudegoed)
        correct = antwoord == goedeantwoord
        
        context = self.get_context_data(form=form)
        nvragen = int(form.data['nvragen']) + 1
        ngoed = int(form.data['ngoed']) + (1 if correct else 0)
        perc = 10 + nvragen*90/20
        
        context.update(locals())
        
        return self.render_to_response(context)
        
class GemeenteView(ChoiceView):
    def get_objects(self):
        return StreekWijn.objects.exclude(subregion__isnull=True)
    def get_goed(self, objects):
        return objects.exclude(gemeente__isnull=True).exclude(gemeente="").order_by('?')[0]
    def optie_text(self, goed):
        return goed.subregion
    def get_afleiders(self, objects, goed):
        return objects.exclude(subregion=goed.subregion).only("subregion").distinct().values_list("subregion", flat=True)
    def get_vraag(self, goed):
        return "In welke subregio ligt {goed.gemeente}".format(**locals())

class AppellationView(ChoiceView):
    def get_objects(self):
        return StreekWijn.objects.exclude(gemeente__isnull=True).exclude(appellation__isnull=True)
    def get_goed(self, objects):
        return objects.order_by('?')[0]
    def optie_text(self, goed):
        return goed.gemeente
    def get_afleiders(self, objects, goed):
        return objects.exclude(gemeente=goed.gemeente).only("gemeente").distinct().values_list("gemeente", flat=True)
    def get_vraag(self, goed):
        return "In welke gemeente ligt {goed.appellation}".format(**locals())

def subregios2(request, land):
    subregios = StreekWijn.objects.exclude(subregion__isnull=True).exclude(region="")
    if land != "all":
        subregios = subregios.filter(land=land)
    vraag = subregios.order_by('?')[0]
    
    afleiders = list(subregios.only("region").filter(land=vraag.land).distinct().values_list("region", flat=True))
    afleiders.remove(vraag.region)
    shuffle(afleiders)
    keuzes = afleiders[:3] + [vraag.region]
    shuffle(keuzes)

    if request.POST:
        oudevraag = request.POST["vraag"]
        oudevraag = StreekWijn.objects.get(pk=oudevraag)
        
        keuze = request.POST["region"]
        goed = (keuze == oudevraag.region)

        nvragen = int(request.POST["nvragen"]) + 1
        ngoed = int(request.POST["ngoed"])
        if goed:
            ngoed = ngoed + 1
        perc = 10 + nvragen*90/20

        if nvragen == 20:
            user = request.user if request.user.is_authenticated() else None
            Score.objects.create(vraag='Subregios2', region=regio, user=user, score=ngoed)
        
    else:
        nvragen = 0
        ngoed = 0

        
    return render(request, 'wijn/subregios2.html', locals())


    

def kleurstring(ap):
    kleurap = ", ".join([a for a in ["rood", "wit", "rose", "mousserend", "zoet"]
                         if getattr(ap, a)]).title()
    if "," in kleurap:
        kleurap = " en ".join(kleurap.rsplit(", ", 1))
    else:
        kleurap = "alleen {kleurap}".format(**locals())
    return kleurap

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

def scores(request):
    best = {}
    my_best = {}
    last = {}
    my_last = {}

    def beats(new, existing):
        if existing is None: return True
        if new.score > existing.score: return True
        if new.score == existing.score: return new.timestamp < existing.timestamp

    for s in Score.objects.all():
        vraag = s.vraag.lower()
        if vraag in ['kleurmeerkeuze','regio']:
            s.url = reverse(vraag)
        else:
            s.url = reverse(vraag, args=[s.region])
        key = s.vraag, s.region
        if request.user.is_authenticated() and s.user == request.user:
            if beats(s, my_best.get(key)):
                my_best[key] = s
            if (key not in my_last) or (my_last[key].timestamp < s.timestamp):
                my_last[key] = s

        if beats(s, best.get(key)):
            best[key] = s
        if (key not in last) or (last[key].timestamp < s.timestamp):
            last[key] = s

    return render(request, 'wijn/scores.html', locals())

