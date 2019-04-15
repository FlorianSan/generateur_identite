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
# récupère toutes les données de la table commentaire


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
# ajoute un commentaire dans la table commentaire


def add_liste(nom, message, email):
    msg = ""
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO commentaires (nom, comment, email) VALUES (%s, %s, %s);"
        param = (nom, message, email)
        cursor.execute(sql, param)
        cnx.commit()
    except mysql.connector.Error as err:
        msg = "Failed add_commentData : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return msg


###################################################################################################
# supprime un commentaire dans la table commentaire


def del_commentData(id_comment):
    msg = ""
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "DELETE FROM commentaires WHERE id_comment=%s;"
        param = (id_comment,)
        cursor.execute(sql, param)
        cnx.commit()
    except mysql.connector.Error as err:
        msg = "Failed del_commentData : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return msg



