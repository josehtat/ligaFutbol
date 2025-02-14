from django.shortcuts import render
from futbol.models import *


def classificacio(request):
    lliga = Lliga.objects.all()[1]
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


