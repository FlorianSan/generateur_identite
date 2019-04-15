import mysql.connector
from mysql.connector import errorcode
import os

NOM = os.path.abspath("fichier_bdd/noms.txt")


config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'identite',
        'raise_on_warnings': True
    }

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

def close_bd(cursor,cnx):
    cursor.close()
    cnx.close()

def add_in_table(filename,table):
    msg = ""
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO "+table+" VALUES (%s);"
        fichier = open(filename, "r")
        for ligne in fichier:
            param = (ligne.split()[0],)
            cursor.execute(sql, param)
            cnx.commit()
        fichier.close()
    except mysql.connector.Error as err:
        msg = "Failed add_commentData : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return msg

print(add_in_table(NOM,"Nom (nom)"))