from django.shortcuts import render, redirect
from django import forms
from futbol.models import *
from django.db import models
from futbol.models import Jugador

class MenuForm(forms.Form):
    lligueta = forms.ModelChoiceField(queryset=Lliga.objects.all())
    dades = forms.CharField(required=False)

class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = "__all__"

class LligaForm(forms.ModelForm):
    class Meta:
        model = Lliga
        fields = "__all__"

def nou_jugador(request):
    if request.method == 'POST':
        form = JugadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nou_jugador')
    else:
        form = JugadorForm()
    return render(request, "menu.html", {"form": form})


def pichichis(request):
    jugadors = []
    form = LligaForm()
    if request.method == "POST":
        form = LligaForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lligueta")
            gs = Jugador.objects.filter(equip_lliga=lliga).order_by('-goles')
            for jugador in gs:
                jugadors.append({"jugador": jugador.nombre, "goles": jugador.gols})
    return render(request, "pichichi.html", {"jugadors": jugadors, "form": form})

def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lligueta")
            # cridem a /classificacio/<lliga_id>
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })


def classificacio(request, lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
    equips = lliga.equips.all()
    classi = []
    
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partits.filter(equip_local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partits.filter(equip_visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1

        goles_favor_total = 0
        goles_contra_total = 0
        diferencia_goles_total = 0

        for partit in lliga.partits.filter(equip_local=equip) | lliga.partits.filter(equip_visitant=equip):
            if partit.equip_local == equip:
                goles_favor_total += partit.gols_local()
                goles_contra_total += partit.gols_visitant()
            else:
                goles_favor_total += partit.gols_visitant()
                goles_contra_total += partit.gols_local()
            diferencia_goles_total += partit.gols_local() - partit.gols_visitant()
            

        victorias_total = 0
        derrotas_total = 0
        empates_total = 0

        for partit in lliga.partits.filter(equip_local=equip) | lliga.partits.filter(equip_visitant=equip):
            if partit.equip_local == equip:
                if partit.gols_local() > partit.gols_visitant():
                    victorias_total += 1
                elif partit.gols_local() < partit.gols_visitant():
                    derrotas_total += 1
                else:
                    empates_total += 1
            else:
                if partit.gols_visitant() > partit.gols_local():
                    victorias_total += 1
                elif partit.gols_visitant() < partit.gols_local():
                    derrotas_total += 1
                else:
                    empates_total += 1

        classi.append( {"punts":punts, "equip":equip.nom, "goles_favor":goles_favor_total, "goles_contra":goles_contra_total, "diferencia_goles":diferencia_goles_total, "victorias":victorias_total, 
                        "derrotas":derrotas_total, "empates":empates_total } )
    # ordenem llista
    classi.sort(reverse=True, key=lambda x: x["punts"])
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "nom_lliga":lliga.nom 
                })


