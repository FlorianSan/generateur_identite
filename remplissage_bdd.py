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

def add_liste_base():
    msg = "Import de la liste de base"
    try:
        cnx = connexion()
        cursor = cnx.cursor()
        sql = "INSERT INTO Liste_fiche(descriptif, dim, idUtilisateur) VALUE ('Liste de base','3','1');"
        cursor.execute(sql)
        sql = "INSERT INTO Individu(idNom, idPrenom, date_naissance, ville_naissance, idResidence, numero_insee, mrz, numTel, num_carte_banc, email, iban, genre, idBanque, idListe) VALUE ('38745','10413','1986-06-25','Balma','85726','18606310445837','IDFRA487609<<<099999999R<<<<<<8606257M3405178FRA<<<<<<<<<<<1CAZU<<WILEY<<<<<<<<<<<<<<<<<<<','0674923591','5165346126100580', 'wiley.cazuc@gmail.com', 'FR2149860706508890690185170','m', '581', '1');"
        cursor.execute(sql)
        sql = "INSERT INTO Individu(idNom, idPrenom, date_naissance, ville_naissance, idResidence, numero_insee, mrz, numTel, num_carte_banc, email, iban, genre, idBanque, idListe) VALUE ('73295','9053','2019-04-15','Millau','83628','119041214572982','IDFRA339691<<<999999999R<<<<<<1904150M3405178FRA<<<<<<<<<<<7DUPL<<SHAI<<<<<<<<<<<<<<<<<<<<','0689896003','5251014090258290','shai.duplay@gmail.com','FR9086187679502274130821456','m', '599', '1');"
        cursor.execute(sql)
        sql = "INSERT INTO Individu(idNom, idPrenom, date_naissance, ville_naissance, idResidence, numero_insee, mrz, numTel, num_carte_banc, email, iban, genre, idBanque, idListe) VALUE ('75890', '2225', '1977-03-25', 'Bérat', '41615', '17703310654193', 'IDFRA215345<<<099999999R<<<<<<7703252M3405178FRA<<<<<<<<<<<5ENG<<DARNELL<<<<<<<<<<<<<<<<<<','0641145407','5576934464708660', 'wiley.cazuc@gmail.com','FR0418902570981964603690392','m', '57', '1');"
        cursor.execute(sql)
        cnx.commit()

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
    print(add_liste_base())