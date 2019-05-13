#! C:\Program Files (x86)\Python\Python37\python.exe
# -*- coding: UTF-8 -*-
# enable debugging

from flask import session
from app.data.bdd import *
from random import randint
from mrz.generator.td1 import TD1CodeGenerator
from datetime import date


###################################################################################################


def create_identites(dataform):
    nombre = int(dataform['nombre'])
    description = dataform['description']
    idliste = insert_liste(description,session['id'])
    numprenommax, numnommax, numresidencemax, numbanqmax = get_dim()
    for i in range(nombre):
        idprenom = randint(1,numprenommax)
        idnom = randint(1, numnommax)
        idresidence = randint(1, numresidencemax)
        idvillenaissance = randint(1, numresidencemax)
        idbanque = randint(1, numbanqmax)
        nom, prenom, genre, residence, banq, ville_naissance = get_info(idprenom, idnom, idresidence, idbanque, idvillenaissance)
        email = str(prenom) + "." + str(nom) + "@gmail.com"
        numero_insee = "1"
        numTel ="0638922520"
        num_carte_banc = "10"
        iban = "15"
        date_naissance = "1998-06-04"
        #mrz = str(TD1CodeGenerator("ID","FRA","BAA000589", "800101", "F", "250101", "FRA", "ESPAÑOLA ESPAÑOLA", "CARMEN", "99999999R"))
        mrz="10"
        insert_identite((idnom, idprenom, date_naissance, ville_naissance, idresidence, numero_insee, mrz,  numTel, num_carte_banc, email, iban, genre, idbanque, idliste))
    return


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


