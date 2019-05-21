#! C:\Program Files (x86)\Python\Python37\python.exe
# -*- coding: UTF-8 -*-
# enable debugging

from flask import session
from app.data.bdd import *
from random import randint, randrange
from mrz.generator.td1 import TD1CodeGenerator
from datetime import date, timedelta
from schwifty import IBAN

from app.controllers.carte_identite import credit_card_number
import time
import os

FICHIER_TEXTE = os.path.abspath("app/static/export.txt")
pourcentage = 0
###################################################################################################


def create_identites(dataform):
    global pourcentage
    type = dataform['btn_submit']
    nombre = int(dataform['nombre'])

    numprenommax, numnommax, numresidencemax, numbanqmax = get_dim()

    if type == "creer":
        description = dataform['description']
        idliste = insert_liste(description,nombre,session['id'])
        for i in range(nombre):
            insert_identite(create_identite(numprenommax, numnommax, numresidencemax, numbanqmax, dataform)[0] + (idliste,))
            pourcentage= (i / nombre) * 100
    else:
        separateur = str(dataform["separateur"])
        with open(FICHIER_TEXTE, "w") as fichier:
            for i in range(nombre):
                info = create_identite(numprenommax, numnommax, numresidencemax, numbanqmax, dataform)[1]
                print(info)
                fichier.write( str(info[0]) + separateur + str(info[1]) + separateur + str(info[2]).replace("-","/") + separateur + str(info[3]) + separateur + str(info[4][0]) + separateur + str(info[4][1]) + separateur + str(info[4][2]) + separateur + str(info[4][3]) + separateur + str(info[5]) + separateur + str(info[6]) + separateur + str(info[7]) + separateur + str(info[8]) + separateur + str(info[9]) + separateur + str(info[10]) + separateur + str(info[11]) + "\n")
                pourcentage = (i / nombre) * 100
    pourcentage = 0
    return type


def generate():
    global pourcentage
    yield "data:" + str(round(pourcentage)) + "\n\n"


def create_identite(numprenommax,numnommax,numresidencemax,numbanqmax, dataform):


    idprenom = randint(1, numprenommax)
    idnom = randint(1, numnommax)
    idbanque = randint(1, numbanqmax)

    if 'datenaiss' in dataform:
        date_naissance = time.strftime('%Y/%m/%d', time.gmtime(randint(0, int(time.time()))))
    else:
        date_naissance = None

    if 'ville_naissance'in dataform:
        idvillenaissance = randint(1, numresidencemax)
    else:
        idvillenaissance = None

    if 'adresse' in dataform:
        idresidence = randint(1, numresidencemax)
    else:
        idresidence = None

    nom, prenom, genre, residence, banq, ville_naissance = get_info(idprenom, idnom, idresidence, idbanque,
                                                                    idvillenaissance)

    if not(ville_naissance):
        ville_naissance = None
    if 'numero_insee'in dataform:
        num=[]
        if genre == 'm':
            num.append('1')
        else:
            num.append('2')
        num.append(str(date_naissance[2:4]))
        num.append(str(date_naissance[5:7]))
        num.append(str(ville_naissance[2]))
        num.append(str(n_len_rand(3)))
        cle = 97 - (int(''.join(num))%97)
        num.append(str(cle))
        numero_insee = str(''.join(num))

    else:
        numero_insee = None

    if 'idcard'in dataform:
        mrz = str(TD1CodeGenerator("ID", "FRA", str(randint(1, 1000000)), date_naissance.replace("/","")[2:], str.upper(genre)[0],
                                   str(date.today() + timedelta(days=5475)).replace("-", "")[2:],
                                   "FRA", nom[:4] , prenom[:29], "99999999R")).replace('\n', "")

    else:
        mrz = None

    if 'numTel' in dataform:
        num = ['0', '6']
        for i in range(8):
            num.append(str(randint(0, 9)))
        numTel = str(''.join(num))
    else:
        numTel = None

    if 'email' in dataform:
        email = str(prenom) + "." + str(nom).lower()+ "@gmail.com"
    else:
        email = None

    if 'num_carte_banc' in dataform:
        num_carte_banc = str(credit_card_number())
    else:
        num_carte_banc = None

    if 'iban' in dataform:
        compte = str(randint(1, 1000000000000000000))
        bank_code = str(randint(10000, 99999))
        iban = str(IBAN.generate('FR', bank_code=bank_code, account_code=compte))
    else:
        iban = None
    return (idnom, idprenom, date_naissance, ville_naissance[0], idresidence, numero_insee, mrz,  numTel, num_carte_banc, email, iban, genre, idbanque),(nom, prenom, date_naissance, ville_naissance[0], residence,  numero_insee, mrz,  numTel, num_carte_banc, email, iban, genre,)




def verif_connect(dataform):
    login = dataform["login"]
    mdp = dataform["MDP"]
    res = authentification(login, mdp)
    try:
        session["id"] = res[0]["idUtilisateur"]
        session["privilege"] = res[0]["privilege"]
        session["login"] = res[0]["login"]
        session["logged_in"] = 1
        page_redirect = ["index","auth_success"]
    except(KeyError, IndexError) as e:
        page_redirect = ["login", "auth_fail"]
    return page_redirect


def remove_liste(dataform):
    idListe = dataform["btn_submit"]
    remove_oneListe(idListe)

def visu_liste(dataform):
    idListe = dataform["btn_visualiser"]
    nombre = int(dataform["nombre"])
    oneliste = get_oneListe(idListe)[:nombre]
    for i in range(len(oneliste)):
        if not('datenaiss') in dataform:
            del oneliste[i]["date_naissance"]
        if not ('ville_naissance') in dataform:
            del oneliste[i]["ville_naissance"]
        if not ('adresse') in dataform:
            del oneliste[i]["numero"]
            del oneliste[i]["nom_voie"]
            del oneliste[i]["code_post"]
            del oneliste[i]["nom_commune"]
        if not ('insee') in dataform:
            del oneliste[i]["numero_insee"]
        if not ('idcard') in dataform:
            del oneliste[i]["mrz"]
        if not ('numTel') in dataform:
            del oneliste[i]["numTel"]
        if not ('email') in dataform:
            del oneliste[i]["email"]
        if not ('num_carte_banc') in dataform:
            del oneliste[i]["num_carte_banc"]
        if not ('iban') in dataform:
            del oneliste[i]["iban"]
        if not ('genre') in dataform:
            del oneliste[i]["genre"]
    return oneliste

def preparation_download_liste(dataform):
    idListe = dataform["btn_download"]
    separateur = str(dataform["separateur"])
    liste = get_oneListe(idListe)
    with open(FICHIER_TEXTE, "w") as fichier:
        for i in range(len(liste)):
            fichier.write( str(liste[i]["nom"]) + separateur + str(liste[i]["prenom"]) + separateur + str(liste[i]["date_naissance"]).replace("-","/") + separateur + str(liste[i]["ville_naissance"]) + separateur + str(liste[i]["numero"]) + separateur + str(liste[i]["nom_voie"]) + separateur + str(liste[i]["code_post"]) + separateur + str(liste[i]["nom_commune"]) + separateur + str(liste[i]["numero_insee"]) + separateur + str(liste[i]["mrz"]) + separateur + str(liste[i]["numTel"]) + separateur + str(liste[i]["num_carte_banc"]) + separateur + str(liste[i]["email"]) + separateur + str(liste[i]["iban"]) + separateur + str(liste[i]["genre"]) + "\n")

def n_len_rand(len_, floor=1):
    top = 10**len_
    if floor > top:
        raise ValueError(f"Floor {floor} must be less than requested top {top}")
    return f'{randrange(floor, top):0{len_}}'
