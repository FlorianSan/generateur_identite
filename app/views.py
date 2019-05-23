#! C:\Program Files (x86)\Python\Python37\python.exe
# Filename: views.py
# encoding: utf-8

from flask import render_template, request, redirect, url_for, send_from_directory, Response
from . import app
from app.controllers.formulaire import *
import os
FICHIER_TEXTE = os.path.abspath("app/data/export.txt")

###################################################################################################
# route pour la page d'accueil

@app.route('/')
def index():
    return render_template('index.html')

###################################################################################################
# route pour afficher toutes les listes de la bdd

@app.route('/liste')
def liste():
    liste_id = get_allListe()
    return render_template('liste.html', data=liste_id)

###################################################################################################
#route pour afficher les listes en fonction de la selection

@app.route('/sublist',methods = ['POST', 'GET'])
def sublist():
    one_liste = visu_liste(request.form)
    return render_template('sublist.html', data=one_liste)

###################################################################################################
#route pour ouvrir la page de selection des informations à visualiser en rapport avec la liste choisi

@app.route('/selecteur',methods = ['POST', 'GET'])
def selecteur():
    idListe = request.form["btn_visualiser"]
    return render_template('selecteur.html', data=(idListe,))

###################################################################################################
#route créer une liste d'identité et qui en fonction de la connection ouvre la page liste.html ou télécharge la liste

@app.route('/formulaire_creation',methods = ['POST', 'GET'])
def formulaire_creation():
    type = create_identites(request.form)
    if type == "creer":
        return redirect(url_for('liste'))
    else:
        return send_from_directory(directory='static', filename='export.txt', as_attachment=True)

###################################################################################################
#route pour supprimer une liste

@app.route('/delete_liste',methods = ['POST', 'GET'])
def delete_liste():
    remove_liste(request.form)
    return redirect(url_for('liste'))

###################################################################################################
#route pour télécharger une liste

@app.route('/download_liste',methods = ['POST', 'GET'])
def download_liste():
    preparation_download_liste(request.form)
    return send_from_directory(directory='static', filename='export.txt', as_attachment=True)

###################################################################################################
#route pour tester la connexion

@app.route('/connexion',methods = ['POST', 'GET'])
def connexion():
    page_redirect = verif_connect(request.form)
    return  redirect(url_for(page_redirect[0],info=page_redirect[1]))

###################################################################################################
#route qui envoye vers la page de connexion

@app.route('/login')
def login():
    return render_template('connecter.html')

###################################################################################################
#route qui envoye vers la page de creation de liste

@app.route('/create')
def create():
    return render_template('creer.html')

###################################################################################################
#route qui permet la mise à jour de la barre de progression

@app.route('/progress')
def progress():
	return Response(generate(), mimetype= 'text/event-stream')

###################################################################################################
#route vers la deconnexion

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

###################################################################################################
#route qui envoye vers la page de webmaster

@app.route('/webmaster')
def webmaster():
   return render_template('webmaster.html')

###################################################################################################
#route qui envoye vers la page du cv1

@app.route('/cv1')
def cv1():
   return render_template('cv1.html')

###################################################################################################
#route qui envoye vers la page du cv2

@app.route('/cv2')
def cv2():
   return render_template('cv2.html')

###################################################################################################
#route qui envoye vers la page du cv3

@app.route('/cv3')
def cv3():
   return render_template('cv3.html')