#! C:\Program Files (x86)\Python\Python37\python.exe
# -*- coding: UTF-8 -*-
# enable debugging

from flask import session
from app.data.bdd import *


###################################################################################################
#ajoute un commentaire dans la BD

def create_liste(dataform):
    nombre = dataform['nombre']


    info = "insComment_success"
    msg=add_liste()
    if msg != "":
        info="insComment_fail"

    return info


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
