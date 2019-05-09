#! C:\Program Files (x86)\Python\Python37\python.exe
# -*- coding: UTF-8 -*-
# enable debugging

import mysql.connector
from mysql.connector import errorcode


config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'identite',
        'raise_on_warnings': True
    }

#################################################################################################################
#connexion au serveur de la base de données


def connexion():
    cnx = ""
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Mauvais login ou mot de passe pour la bdd")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La Base de données n'existe pas.")
        else:
            print(err)
    return cnx


#################################################################################################################
#fermeture de la connexion au serveur de la base de données


def close_bd(cursor,cnx):
    cursor.close()
    cnx.close()



###################################################################################################
# transforme le résultat de la requete select en dictionnaire ayant pour index le nom des colonnes de la table en BD

def convert_dictionnary(cursor):
    columns = cursor.description
    result = []
    # reception des données sous forme de dictionnaire avec le nom des colonnes.
    for value in cursor.fetchall():
        tmp = {}
        for (index, column) in enumerate(value):
            tmp[columns[index][0]] = column
        result.append(tmp)
    return result

###################################################################################################
# teste l'authentification


def authentification(login,mdp):

    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "SELECT * FROM utilisateur WHERE login=%s AND mdp=%s LIMIT 1"
        param = (login, mdp)
        cursor.execute(sql, param)
        res = convert_dictionnary(cursor)
    except mysql.connector.Error as err:
        res = "Failed authentification : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return res


###################################################################################################
# récupère toutes les liste


def get_allListe():

    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "SELECT * FROM liste_fiche AS lf JOIN Utilisateur AS U ON U.idUtilisateur = lf.idUtilisateur "
        cursor.execute(sql)
        res = convert_dictionnary(cursor)
    except mysql.connector.Error as err:
        res = "Failed get data : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return res

###################################################################################################
# recuperer la dimension  de tables de la bdd


def get_dim():
    try:

        cnx = connexion()
        cursor = cnx.cursor()
        sql = "SELECT COUNT(idNom) FROM nom"
        cursor.execute(sql)
        numnom = cursor.fetchall()[0][0]
        sql = "SELECT COUNT(idPrenom) FROM prenom"
        cursor.execute(sql)
        numprenom = cursor.fetchall()[0][0]
        sql = "SELECT COUNT(idBanque) FROM banque"
        cursor.execute(sql)
        numbanq = cursor.fetchall()[0][0]
        sql = "SELECT COUNT(idResidence) FROM residence"
        cursor.execute(sql)
        numresidence = cursor.fetchall()[0][0]
        close_bd(cursor, cnx)
        return numprenom, numnom, numresidence, numbanq
    except mysql.connector.Error as err:
        close_bd(cursor, cnx)
        return "Failed get data : {}".format(err)

def get_info(idprenom, idnom, idresidence, idbanq, idvillenaissance):
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "SELECT nom FROM nom WHERE idNom=%s"
        cursor.execute(sql,(idnom,))
        nom = cursor.fetchall()[0][0]
        sql = "SELECT prenom, genre FROM prenom WHERE idPrenom=%s"
        cursor.execute(sql,(idprenom,))
        prenom = cursor.fetchall()[0]
        sql = "SELECT refBanque FROM banque WHERE idbanque=%s"
        cursor.execute(sql,(idbanq,))
        banque = cursor.fetchall()[0][0]
        sql = "SELECT numero, nom_voie, code_post, nom_commune FROM residence WHERE idResidence=%s"
        cursor.execute(sql,(idresidence,))
        adresse = cursor.fetchall()[0]
        sql = "SELECT nom_commune FROM residence WHERE idResidence=%s"
        cursor.execute(sql, (idvillenaissance,))
        ville_naissance = cursor.fetchall()[0][0]
        close_bd(cursor, cnx)
        return nom, prenom, adresse, banque, ville_naissance
    except mysql.connector.Error as err:
        close_bd(cursor, cnx)
        return "Failed get data : {}".format(err)

def create_liste(info):
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO liste_fiche(descriptif, idUtilisateur) VALUE (%s,%s);"
        cursor.execute(sql, info)
        sql = "SELECT idListe FROM liste_fiche WHERE descriptif=%s;"
        cursor.execute(sql, info[0])
        idliste = cursor.fetchall()[0][0]
    except mysql.connector.Error as err:
        print("Failed get data : {}".format(err))
    finally:
        close_bd(cursor, cnx)
    return idliste

def create_identite(info):
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO individu(idNom , idPrenom, date_naissance, ville_naissance, idResidence, numero_insee, mrz, numTel, num_carte_banc, email, iban, genre, idBanque, idListe) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(sql, info)
    except mysql.connector.Error as err:
        print("Failed get data : {}".format(err))
    finally:
        close_bd(cursor, cnx)
    return