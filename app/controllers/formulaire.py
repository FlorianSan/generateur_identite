#! C:\Program Files (x86)\Python\Python37\python.exe
# -*- coding: UTF-8 -*-
# enable debugging

from flask import session
from app.data.bdd import *
from random import randint
from mrz.generator.td1 import TD1CodeGenerator
from datetime import date, timedelta
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
            print(create_identite(numprenommax, numnommax, numresidencemax, numbanqmax, dataform)[0] + (idliste,))
            insert_identite(create_identite(numprenommax, numnommax, numresidencemax, numbanqmax, dataform)[0] + (idliste,))

            pourcentage= (i / nombre) * 100
    else:
        with open(FICHIER_TEXTE, "w") as fichier:
            for i in range(nombre):
                fichier.write(str(create_identite(numprenommax, numnommax, numresidencemax, numbanqmax, dataform)[1])+"\n")
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
        date_naissance = "1998-06-04"
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
        numero_insee = "1"
    else:
        numero_insee = None

    if 'idcard'in dataform:
        mrz = str(TD1CodeGenerator("ID", "FRA", "BAA000589", "800101", "F",
                                   str(date.today() + timedelta(days=5475)).replace("-", "")[2:],
                                   "FRA", "ESPAÑOLA ESPAÑOLA", "CARMEN", "99999999R")).replace('\n', "")
    else:
        mrz = None

    if 'numTel' in dataform:
        numTel = "0638922520"
    else:
        numTel = None

    if 'email' in dataform:
        email = str(prenom) + "." + str(nom).lower()+ "@gmail.com"
    else:
        email = None

    if 'num_carte_banc' in dataform:
        num_carte_banc = "111555"
    else:
        num_carte_banc = None

    if 'iban' in dataform:
        iban = "15"
    else:
        iban = None
    return (idnom, idprenom, date_naissance, ville_naissance, idresidence, numero_insee, mrz,  numTel, num_carte_banc, email, iban, genre, idbanque),(nom, prenom, date_naissance, genre, residence, banq, ville_naissance, numero_insee, mrz,  numTel, num_carte_banc, email, iban)




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
    oneliste = get_oneListe(idListe)
    return oneliste[:nombre]

def preparation_download_liste(dataform):
    idListe = dataform["btn_download"]
    liste = get_oneListe(idListe)
    with open(FICHIER_TEXTE, "w") as fichier:
        for i in range(len(liste)):
            fichier.write(str(liste[i])+"\n")
