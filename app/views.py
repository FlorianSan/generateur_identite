#! C:\Program Files (x86)\Python\Python37\python.exe
# Filename: views.py
# encoding: utf-8

from flask import render_template, request, redirect, url_for
from . import app
from app.controllers.formulaire import *
from app.controllers.functions import *


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/liste')
def liste():
    liste_id = get_allListe()
    return render_template('liste.html', data=liste_id)

@app.route('/formulaire_creation',methods = ['POST', 'GET'])
def formulaire_creation():
    info_add = create_identites(request.form)
    return redirect(url_for('liste'))

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

@app.route('/logout')
def logout():
   session.clear()
   return redirect(url_for('index'))



