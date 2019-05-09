#! C:\Program Files (x86)\Python\Python37\python.exe
# -*- coding: UTF-8 -*-
# enable debugging

from flask import session
from app.data.bdd import *
from random import randint
from mrz.generator.td1 import TD1CodeGenerator
from datetime import date


###################################################################################################


def create_liste(dataform):
    nombre = int(dataform['nombre'])
    description = dataform['description']
    idliste = create_liste((description,session('id')))
    numprenommax, numnommax, numresidencemax, numbanqmax = get_dim()
    for i in range(nombre):
        idprenom = randint(1,numprenommax)
        idnom = randint(1, numnommax)
        idresidence = randint(1, numresidencemax)
        idvillenaissance = randint(1, numresidencemax)
        idbanque = randint(1, numbanqmax)
        prenom_genre,nom,residence,banq,ville_naissance =  get_info(idprenom, idnom, idresidence, idbanque, idvillenaissance)
        email = prenom_genre[0] + "." + nom + "@gmail.com"
        genre= prenom_genre[1]

        mrz = TD1CodeGenerator("ID","FRA","BAA000589",  # Document number "800101",  # Birth date      YYMMDDstr.upper(prenom_genre[1]),  # Genre           Male: 'M', Female: 'F' or Undefined 'X'date.today(),  # Expiry date     YYMMDD
                         #"FRA",  # Nationality
                         #"ESPAÑOLA ESPAÑOLA",  # Surname         Special characters will be transliterated
                         #"CARMEN",  # Given name(s)   Special characters will be transliterated
                         #"99999999R")  # Optional data 1

        create_identite((idnom, idprenom, date_naissance, idvillenaissance, idresidence, numero_insee, mrz,  numTel, num_carte_banc, email, iban, genre, idbanque, idliste))
    return


def verif_connect(dataform):
    login = dataform["login"]
    mdp = dataform["MDP"]
    res = authentification(login, mdp)
    try:
        session["id"] = res[0]["idUtilisateur"]
        session["nom"] = res[0]["privilege"]
        session["prenom"] = res[0]["login"]
        session["logged_in"] = 1
        page_redirect = ["index","auth_success"]
    except(KeyError, IndexError) as e:
        page_redirect = ["login", "auth_fail"]
    return page_redirect


