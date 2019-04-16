import mysql.connector
from mysql.connector import errorcode
import os
from math import ceil

NOM = os.path.abspath("fichier_bdd/noms.txt")
PRENOM = os.path.abspath("fichier_bdd/prenoms.txt")

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

def add_nom():
    msg = "Succes"
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO Nom (nom) VALUES (%s);"
        fichier = open(NOM, "r")
        l=[]
        for ligne in fichier:
            data = (ligne.split()[0],)
            l.append(data)
        cursor.executemany(sql, l[:80000])
        cursor.executemany(sql, l[80000:160000])
        cursor.executemany(sql, l[160000:])
        cnx.commit()
        fichier.close()
    except mysql.connector.Error as err:
        msg = "Failed add_in_table : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return msg

def add_prenom():
    msg = "Succes"
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO Prenom (prenom, genre) VALUES (%s, %s);"
        fichier = open(PRENOM, "r")
        l=[]
        for ligne in fichier:
            data = ligne.replace('\x00','').replace('\n','').split("\t")
            if len(data) == 4 :
                d = (data[0],data[1])
                l.append(d)
        cursor.executemany(sql, l)
        cnx.commit()
        fichier.close()
    except mysql.connector.Error as err:
        msg = "Failed add_in_table : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return msg

if __name__ == '__main__':
    print(add_prenom())
    print(add_nom())