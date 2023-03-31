# Kalendri alus võetud https://github.com/Serhioromano/bootstrap-calendar ning kohandatud endale sobivaks

#! python -m pip install Flask
#! python -m pip install flask-cors
#! python -m pip install mysql-connector-python

import flask 
from flask import Flask, jsonify, render_template, request, flash
from flask_cors import CORS
import datetime
import sql 

app=Flask(__name__,template_folder='templates')
app.secret_key = "secret"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=10)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def my_form_post():
    if flask.request.method == 'POST':
        # Andmete vastuvõtmine HTML-ist
        sql.ei_leidu = sql.voetud = sql.vale_nimi = 0
        ruum = request.form['Ruum']
        kuupaev = request.form['Kuupaev']
        aeg = request.form['Kellaaeg']
        nimi = request.form['Nimi']
        # Andmete formaatimine sql.py-i saatmiseks
        kell = aeg
        kell = kell.split('-')
        alguskell = kell[0].split('.')
        alguskell = int(alguskell[0]) * 3600 + int(alguskell[1]) * 60
        alguskell = datetime.timedelta(seconds=alguskell)
        loppkell = kell[1].split('.')
        loppkell = int(loppkell[0]) * 3600 + int(loppkell[1]) * 60
        loppkell = datetime.timedelta(seconds=loppkell)
        kuupaev1 = kuupaev
        kuupaev1 = kuupaev1.split('-')
        kuupaev1 = datetime.date(int(kuupaev1[0]), int(kuupaev1[1]), int(kuupaev1[2]))
        broneering = [kuupaev1, alguskell, loppkell, nimi]
        sql.lisa(ruum, broneering)
        # sql.py muutujate sisse toomine lisamise kontrolliks
        voetud = sql.voetud
        # Kontrollid staatuste kuvamiseks, andmete kontrollimine toimub sql.py-s
        if request.method == 'POST' and voetud == 1:
          flash('Valitud aeg on juba teise kasutaja poolt broneeritud!')
          return flask.render_template("index.html")
        elif request.method == 'POST' and voetud == 0:
            form_data = request.form
            flash('Broneerimine oli edukas!')
            return flask.render_template('submit.html', form_data = form_data) 
        else:
            flash('Broneerimisel tuli tõrge!')
    elif flask.request.method == 'GET':
        return render_template("delete.html")
        
@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if flask.request.method == 'POST':
        # Andmete vastuvõtmine HTML-ist
        ruum = request.form['ruumid']
        kuupaev = request.form['kuupaev']
        aeg = request.form['ajad']
        nimi = request.form['nimi']
        # Andmete formaatimine sql.py-i saatmiseks
        kell = aeg
        kell = kell.split('-')
        alguskell = kell[0].split('.')
        alguskell = int(alguskell[0]) * 3600 + int(alguskell[1]) * 60
        alguskell = datetime.timedelta(seconds=alguskell)
        loppkell = kell[1].split('.')
        loppkell = int(loppkell[0]) * 3600 + int(loppkell[1]) * 60
        loppkell = datetime.timedelta(seconds=loppkell)
        kuupaev1 = kuupaev
        kuupaev1 = kuupaev1.split('-')
        kuupaev1 = datetime.date(int(kuupaev1[0]), int(kuupaev1[1]), int(kuupaev1[2]))
        broneering = [kuupaev1, alguskell, loppkell, nimi]
        sql.eemalda(ruum, broneering)
        # sql.py muutujate sisse toomine kustuamise kontrolliks
        vale_nimi = sql.vale_nimi
        ei_leidu = sql.ei_leidu
        # Kontrollid staatuste kuvamiseks, andmete kontrollimine toimub sql.py-s
        if request.method == 'POST' and vale_nimi == 1:
            flash('Sisestatud nimi ei ühti broneerija nimega!')  
            return flask.render_template("delete.html")
        elif request.method == 'POST' and ei_leidu == 1:
            flash('Broneeringut ei leitud!')  
            return flask.render_template("delete.html")
        elif request.method == 'POST':
            form_data = request.form
            flash('Kustutamine oli edukas!')
            return flask.render_template('delete.html', form_data = form_data)
        else:
            flash('Kustutamisel tuli tõrge!')
    elif flask.request.method == 'GET':
        return render_template("delete.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route('/calendar', methods=['POST', 'GET'])
def calendar():
    if flask.request.method == 'POST':
        # Andmete vastuvõtmine HTML-ist
        ruum = request.form['RUUM']
        # Ruumi edastamine sql.py-sse et importida selle ruumi kohta kirjed
        sql.impordi(ruum)
    return render_template('calendar.html')

@app.route('/calendar-events', methods=['POST', 'GET'])
def calendar_events():
    # Koostada kalendri jaoks sobivas formaadis eventid
    kirjed = sql.broneeringud
    resp = jsonify({'success' : 1, 'result' : kirjed})
    resp.status_code = 200
    return resp

sql.eemalda_vanad()

if __name__ == '__main__':
    app.run(debug=True)