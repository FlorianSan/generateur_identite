#! C:\Program Files (x86)\Python\Python37\python.exe
# -*- coding: UTF-8 -*-
# enable debugging

import mysql.connector
from mysql.connector import errorcode


config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'IENAC18_sansou_thiboult_vanhersecke_identite',
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
        sql = "SELECT * FROM utilisateur WHERE login=%s AND mdp=%s LIMIT 1;"
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
        sql = "SELECT * FROM liste_fiche AS lf JOIN Utilisateur AS U ON U.idUtilisateur = lf.idUtilisateur WHERE lf.idUtilisateur != 2;"
        cursor.execute(sql)
        res = convert_dictionnary(cursor)
    except mysql.connector.Error as err:
        res = "Failed get data : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return res


def get_oneListe(idListe):
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "SELECT nom, prenom, date_naissance, ville_naissance, numero, nom_voie, code_post, nom_commune, numero_insee, mrz, numTel, email, num_carte_banc, iban, I.genre  FROM liste_fiche AS lf JOIN Individu AS I ON I.idListe = lf.idListe JOIN Nom AS N ON N.idNom = I.idNom JOIN prenom AS P ON P.idPrenom=I.idPrenom JOIN banque AS B ON B.idBanque = I.idBanque JOIN residence AS R ON R.idResidence=I.idResidence WHERE lf.idListe = %s;"
        cursor.execute(sql,(idListe,))
        res = convert_dictionnary(cursor)
    except mysql.connector.Error as err:
        print("Failed get data : {}".format(err))
    finally:
        close_bd(cursor, cnx)
    return res


def remove_oneListe(idListe):
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "DELETE FROM liste_fiche WHERE idListe = %s;"
        cursor.execute(sql,(idListe,))
        cnx.commit()
    except mysql.connector.Error as err:
        print("Failed get data : {}".format(err))
    finally:
        close_bd(cursor, cnx)
    return

###################################################################################################
# recuperer la dimension  de tables de la bdd


def get_dim():
    try:

        cnx = connexion()
        cursor = cnx.cursor()
        sql = "SELECT COUNT(idNom) FROM nom;"
        cursor.execute(sql)
        numnom = cursor.fetchall()[0][0]
        sql = "SELECT COUNT(idPrenom) FROM prenom;"
        cursor.execute(sql)
        numprenom = cursor.fetchall()[0][0]
        sql = "SELECT COUNT(idBanque) FROM banque;"
        cursor.execute(sql)
        numbanq = cursor.fetchall()[0][0]
        sql = "SELECT COUNT(idResidence) FROM residence;"
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
        sql = "SELECT prenom, genre FROM prenom WHERE idPrenom=%s;"
        cursor.execute(sql,(idprenom,))
        prenom,genre = cursor.fetchall()[0]
        sql = "SELECT refBanque FROM banque WHERE idbanque=%s;"
        cursor.execute(sql,(idbanq,))
        banque = cursor.fetchall()[0][0]
        sql = "SELECT numero, nom_voie, code_post, nom_commune FROM residence WHERE idResidence=%s;"
        cursor.execute(sql,(idresidence,))
        adresse = cursor.fetchall()
        if len(adresse)==1:
            adresse = adresse[0]
        sql = "SELECT nom_commune, code_post, code_insee FROM residence WHERE idResidence=%s;"
        cursor.execute(sql, (idvillenaissance,))
        ville_naissance = cursor.fetchall()
        if len(ville_naissance) == 1:
            ville_naissance = ville_naissance[0]
        close_bd(cursor, cnx)
        return nom, prenom, genre, adresse, banque, ville_naissance
    except mysql.connector.Error as err:
        close_bd(cursor, cnx)
        return "Failed get data : {}".format(err)

def insert_liste(description,nombre, idUtilisateur):
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO liste_fiche(descriptif, dim, idUtilisateur) VALUE (%s,%s,%s);"
        cursor.execute(sql, (description,nombre,idUtilisateur))
        cnx.commit()
        sql = "SELECT idListe FROM liste_fiche WHERE descriptif = %s;"
        cursor.execute(sql, (description,))
        idliste = cursor.fetchall()[0][0]
    except mysql.connector.Error as err:
        print("Failed get data : {}".format(err))
    finally:
        close_bd(cursor, cnx)
    return idliste

def insert_identite(info):
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO individu(idNom , idPrenom, date_naissance, ville_naissance, idResidence, numero_insee, mrz, numTel, num_carte_banc, email, iban, genre, idBanque, idListe) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(sql, info)
        cnx.commit()
    except mysql.connector.Error as err:
        print("Failed post data : {}".format(err))
    finally:
        close_bd(cursor, cnx)
    return
