import mysql.connector
from mysql.connector import errorcode
import os
import re

NOM = os.path.abspath("fichier_bdd/noms.txt")
PRENOM = os.path.abspath("fichier_bdd/prenoms.txt")
BANQUES = os.path.abspath("fichier_bdd/banques.txt")

config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'IENAC18_identite',
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
    msg = "Import des noms réussi"
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO Nom (nom) VALUES (%s);"
        fichier = open(NOM, "r", encoding='UTF_8')
        l=[]
        for ligne in fichier:
            data = (ligne.split()[0],)
            if re.match("^[a-z]+$", data[0], flags=re.IGNORECASE):
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
    msg = "Import des prenoms réussi"
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO Prenom (prenom, genre) VALUES (%s, %s);"
        fichier = open(PRENOM, "r", encoding='UTF_8')
        l=[]
        for ligne in fichier:
            data = ligne.replace('\x00','').replace('\n','').split("\t")
            if len(data) == 4 :
                d = (data[0],data[1])
                if re.match("^[a-z]+$", d[0], flags=re.IGNORECASE):
                    l.append(d)
        cursor.executemany(sql, l)
        cnx.commit()
        fichier.close()
    except mysql.connector.Error as err:
        msg = "Failed add_in_table : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return msg

def add_banque():
    msg = "Import des banques réussi"
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO Banque (refBanque) VALUES (%s);"
        fichier = open(BANQUES, "r", encoding='UTF_8')
        l=[]
        for ligne in fichier:
            data = ligne.replace('\x00','').replace('\n','').split("\t")
            if len(data) > 4 :
                d = (data[12],)
                l.append(d)
        l=set(l)
        cursor.executemany(sql, l)
        cnx.commit()
        fichier.close()
    except mysql.connector.Error as err:
        msg = "Failed add_in_table : {}".format(err)
    finally:
        close_bd(cursor, cnx)
    return msg

def add_residence():
    msg = "Import des adresse réussi"
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO Residence (numero, nom_voie, code_post, nom_commune, code_insee) VALUES (%s, %s, %s, %s, %s);"
        for num in [12,46,31]:
            fichier = open('fichier_bdd/BAN_licence_gratuite_repartage_'+str(num)+'.txt', "r", encoding='UTF_8')
            l=[]
            for ligne in fichier:
                data = ligne.replace('\x00','').replace('\n','').split(";")
                if data[3] and data[1] and data[6] and data[15]:
                    d = (data[3],data[1],data[6],data[15],data[5])
                    l.append(d)
            cursor.executemany(sql, l[:10000])
            cursor.executemany(sql, l[10000:20000])
            cursor.executemany(sql, l[20000:30000])
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
    print(add_banque())
    print(add_residence())