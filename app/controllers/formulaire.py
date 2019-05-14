#! C:\Program Files (x86)\Python\Python37\python.exe
# -*- coding: UTF-8 -*-
# enable debugging

from flask import session
from app.data.bdd import *
from random import randint
from mrz.generator.td1 import TD1CodeGenerator
from datetime import date, timedelta
import os

FICHIER_TEXTE = os.path.abspath("app/static/export.txt")

###################################################################################################


def create_identites(dataform):
    type = dataform['btn_submit']
    nombre = int(dataform['nombre'])

    numprenommax, numnommax, numresidencemax, numbanqmax = get_dim()
    if type == "creer":
        description = dataform['description']
        idliste = insert_liste(description,nombre,session['id'])
        for i in range(nombre):
            print(create_identite(numprenommax, numnommax, numresidencemax, numbanqmax,idliste))
            insert_identite(create_identite(numprenommax, numnommax, numresidencemax, numbanqmax,idliste))
    else:
        with open(FICHIER_TEXTE, "w") as fichier:
            for i in range(nombre):
                fichier.write(str(create_identite(numprenommax, numnommax, numresidencemax, numbanqmax))+"\n")
    return type

def create_identite(numprenommax,numnommax,numresidencemax,numbanqmax,idliste):
    idprenom = randint(1, numprenommax)
    idnom = randint(1, numnommax)
    idresidence = randint(1, numresidencemax)
    idvillenaissance = randint(1, numresidencemax)
    idbanque = randint(1, numbanqmax)
    nom, prenom, genre, residence, banq, ville_naissance = get_info(idprenom, idnom, idresidence, idbanque,
                                                                    idvillenaissance)
    email = str(prenom) + "." + str(nom).lower()+ "@gmail.com"
    numero_insee = "1"
    numTel = "0638922520"
    num_carte_banc = "10"
    iban = "15"
    date_naissance = "1998-06-04"
    mrz = str(TD1CodeGenerator("ID", "FRA", "BAA000589", "800101", "F",
                               str(date.today() + timedelta(days=5475)).replace("-", "")[2:],
                               "FRA", "ESPAÑOLA ESPAÑOLA", "CARMEN", "99999999R")).replace('\n',"")
    return (idnom, idprenom, date_naissance, ville_naissance, idresidence, numero_insee, mrz,  numTel, num_carte_banc, email, iban, genre, idbanque, idliste)

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

def preparation_download_liste(dataform):
    idListe = dataform["btn_download"]
    liste = get_oneListe(idListe)
    with open(FICHIER_TEXTE, "w") as fichier:
        for i in range(len(liste)):
            fichier.write(str(liste[i])+"\n")
