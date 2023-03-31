# Abina kasutatud w3schools.com pythoni õpetusi
# Link: https://www.w3schools.com/python/

#! python -m pip install mysql-connector-python

import mysql.connector 
import datetime

voetud = 0
ei_leidu = 0
vale_nimi = 0
broneeringud = []

db = mysql.connector.connect(
  host="mysql.toomas633.com",
  port="3306",
  user="test",
  password="Test-Password01",
  database="school"
)

def impordi(ruum): #Impordi kirjed kalendri vaatesse
  global broneeringud
  broneeringud = []
  cursor = db.cursor()
  # Aegade salvestamiseks
  aeg = []
  # Ajutine kuupaeva ja kellaaja salvestuskoht
  temp = []
  # Impordi kirjed alustade kuupäevade lahtrist ja formaadi raw kuupäeva formaadist ümber loetavaks
  sql = "SELECT kuupäev FROM " + ruum + " ORDER BY kuupäev, alguskell"
  cursor.execute(sql)
  kuupaev = cursor.fetchall()
  i = 0
  k = 0
  for x in kuupaev:
    temp.append([])
    broneeringud.append([])
    broneeringud[i].append('') # ID tuleb siia
    broneeringud[i].append(ruum)
    broneeringud[i].append("")
    broneeringud[i].append("event-info")
    temp[i].append(x[0].strftime("%Y-%m-%d"))
    k += 1
    i += 1
  # Eventide id-de määramine vastavalt kuupäevale
  ajutine_kuupaev = ""
  i = 0
  k = 0
  for x in kuupaev:
    if temp[i][0] > ajutine_kuupaev: # Kui on sama kuupäevaga üritused, lisa id-d järjestikku, kui uus kuupäev, nulli id-d ja alusta lisamist otsast
      ajutine_kuupaev = temp[i][0]
      k = 0
      broneeringud[i][0] = k+1
    else:
      broneeringud[i][0] = k+1
    k += 1
    i += 1
  # Impordi kirjed alguskella lahtrist ja salvesta 24h formaadis
  sql = "SELECT alguskell FROM " + ruum + " ORDER BY kuupäev, alguskell"
  cursor.execute(sql)
  algkell = cursor.fetchall()
  i = 0
  for x in algkell:
    temp[i].append(str(x[0]))
    i += 1
  # Impordi kirjed lõppkella lahtrist ja salvesta 24h formaadis
  sql = "SELECT lõppkell FROM " + ruum + " ORDER BY kuupäev, alguskell"
  cursor.execute(sql)
  loppkell = cursor.fetchall()
  i = 0
  for x in loppkell:
    temp[i].append(str(x[0]))
    i += 1
  # Aegade formaatimine
  temp2 = []
  i = 0
  for x in temp:
    temp2.append([])
    temp2[i].append(temp[i][0] + ' ' + temp[i][1])
    temp2[i].append(temp[i][0] + ' ' + temp[i][2])
    i += 1
  # Aegade lisamine broneeringute nimekirja
  i = 0
  for x in broneeringud:
    broneeringud[i].append(temp2[i][0])
    broneeringud[i].append(temp2[i][1])
    i += 1
  #Aegade vormindamine loetavana kalendris kuvamiseks
  i = 0
  for x in temp:
    aeg1 = temp[i][1].split(':')
    aeg2 = temp[i][2].split(':')
    aeg1 = aeg1[0] + ':' + aeg1[1]
    aeg2 = aeg2[0] + ':' + aeg2[1]
    aeg.append(aeg1 + '-' + aeg2)
    i += 1
  sql = "SELECT nimi FROM " + ruum + " ORDER BY kuupäev, alguskell"
  cursor.execute(sql)
  nimed = cursor.fetchall()
  nimi = []
  for x in nimed:
    nimi.append(x)
  # Aegade vormindamine UNIX timestamp formaati
  # Broneeringute ülekandmine sõnastikku
  temp = broneeringud
  broneeringud = []
  i = 0
  for x in temp:
    start = datetime.datetime.strptime(temp[i][4], "%Y-%m-%d %H:%M:%S")
    start = int(datetime.datetime.timestamp(start) * 1000)
    end = datetime.datetime.strptime(temp[i][5], "%Y-%m-%d %H:%M:%S")
    end = int(datetime.datetime.timestamp(end) * 1000)
    tempd = {
      "id": temp[i][0],
      "title": temp[i][1],
      "url": temp[i][2],
      "class": temp[i][3],
      "start": start,
      "end": end,
      "time": aeg[i],
      "nimi": nimi[i]
    }
    broneeringud.append(tempd)
    i += 1

def lisa(ruum, broneering): # Lisa broneering
  global voetud
  voetud = 0
  cursor = db.cursor()
  # Kontroll kas aeg on vaba
  sql = "SELECT * FROM " + ruum + " WHERE kuupäev = '" + broneering[0].strftime("%Y-%m-%d") + "' AND alguskell = '" + str(broneering[1]) + "' AND lõppkell = '" + str(broneering[2]) + "'"
  cursor.execute(sql)
  olemas = cursor.fetchall()
  print(sql)
  if not olemas: # Kui broneeringut ei leidu
    voetud = 0
    sql = "INSERT INTO " + ruum +" (kuupäev, alguskell, lõppkell, nimi) VALUES ( '" + broneering[0].strftime("%Y-%m-%d") + "','" + str(broneering[1]) + "','" + str(broneering[2]) + "','" + str(broneering[3]) +"')"
    cursor.execute(sql)
    db.commit()
  else: # Kui leidub
    voetud = 1

def eemalda(ruum, broneering): # Eemalda soovitav sissekanne
  global ei_leidu
  global vale_nimi
  vale_nimi = ei_leidu = 0
  cursor = db.cursor()
  # Kontroll kas broneering leidub
  sql = "SELECT * FROM " + ruum + " WHERE kuupäev = '" + broneering[0].strftime("%Y-%m-%d") + "' AND alguskell = '" + str(broneering[1]) + "' AND lõppkell = '" + str(broneering[2]) + "'"
  cursor.execute(sql)
  temp = cursor.fetchall()
  olemas = []
  for x in temp:
    olemas.append(x) 
  try: # Lisatud tühja listi jaoks, vajel tuli index erroreid lihtsalt if lausetega kui broneeringut ei leidunud
    if str(olemas[0][3]) == str(broneering[3]): # Kui nimed ühtivad
      vale_nimi = 0
      ei_leidu = 0
      sql = "DELETE FROM " + ruum + " WHERE kuupäev = '" + broneering[0].strftime("%Y-%m-%d") + "' AND alguskell = '" + str(broneering[1]) + "' AND lõppkell = '" + str(broneering[2]) + "'"
      cursor.execute(sql)
      db.commit()
    elif str(olemas[0][3]) != str(broneering[3]): # Kui nimed ei ühti
      vale_nimi = 1
    else: # muu viga
      print("VIGA sql.py!")
  except: # Kui broneeringut ei leidu
    ei_leidu = 1

def eemalda_vanad(): # Eemlada vanad kirjed
  cursor = db.cursor()
  ruumid = ["A101","A102","A103","A104","A105","A201","A202","A203","A204","A205","A301","B101","B102","B108","B201","B203","B204","B205","B206","B208","B209","B210","C105","C110"]
  kuupaev = datetime.datetime.today() - datetime.timedelta(days=14) #Kui vanad kirjed eemaldatakse 
  kuupaev = kuupaev.strftime("%Y-%m-%d")
  for ruum in ruumid:
    sql = "DELETE FROM " + ruum + " WHERE kuupäev < '" + kuupaev + "'"
    cursor.execute(sql)
    db.commit()

impordi("A101") #Kalendri vaate jaoks esmased andemed