#! C:\Program Files (x86)\Python\Python37\python.exe
# Filename: views.py
# encoding: utf-8

from flask import render_template, request, redirect, url_for, send_from_directory, Response
from . import app
from app.controllers.formulaire import *
import os
FICHIER_TEXTE = os.path.abspath("app/data/export.txt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/liste')
def liste():
    liste_id = get_allListe()
    return render_template('liste.html', data=liste_id)

@app.route('/sublist',methods = ['POST', 'GET'])
def sublist():
    one_liste = visu_liste(request.form)
    return render_template('sublist.html', data=one_liste)

@app.route('/selecteur',methods = ['POST', 'GET'])
def selecteur():
    idListe = request.form["btn_visualiser"]
    return render_template('selecteur.html', data=(idListe,))

@app.route('/formulaire_creation',methods = ['POST', 'GET'])
def formulaire_creation():
    type = create_identites(request.form)
    if type == "creer":
        return redirect(url_for('liste'))
    else:
        return send_from_directory(directory='static', filename='export.txt', as_attachment=True)


@app.route('/delete_liste',methods = ['POST', 'GET'])
def delete_liste():
    remove_liste(request.form)
    return redirect(url_for('liste'))

@app.route('/download_liste',methods = ['POST', 'GET'])
def download_liste():
    preparation_download_liste(request.form)
    return send_from_directory(directory='static', filename='export.txt', as_attachment=True)

@app.route('/connexion',methods = ['POST', 'GET'])
def connexion():
    page_redirect = verif_connect(request.form)
    return  redirect(url_for(page_redirect[0],info=page_redirect[1]))

@app.route('/login')
def login():
    return render_template('connecter.html')

@app.route('/create')
def create():
    return render_template('creer.html')

@app.route('/progress')
def progress():
	return Response(generate(), mimetype= 'text/event-stream')

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('index'))



