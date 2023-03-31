# Ruumide broneerimise süsteem

- [Ruumide broneerimise süsteem](#ruumide-broneerimise-süsteem)
  * [Eesmärk ja kasutatavad vahendid](#eesmärk-ja-kasutatavad-vahendid)
  * [Kasutusjuhend](#kasutusjuhend)
  * [MySQL andmebaas](#mysql-andmebaas)
    + [Andmebaasi andmete formaat](#andmebaasi-andmete-formaat)
    + [Kalendri andmete formaat](#kalendri-andmete-formaat)

## Eesmärk ja kasutatavad vahendid

Projekti eesmärgiks on lihtsustada õppejõudude elu ruumide broneerimisel, et muuta see automaatsemaks, mugavamaks ning vähem aeganõudvamaks.
Projekti loomisel kasutame MySQL-i, Pythonit, HTMLi ja CSSi ning Flaski. Lõpptulemuseks on tegu broneerimissüsteemiga, kuhu tuleb sisestada soovitud kuupäev ja kellaaeg, enda nimi ning valida ruum ja kinnitada broneering. Programm kontrollib üle kas broneering valitud ajaks on võimalik - kui aeg on juba võetud, siis ei viida broneeringut lõpuni. Samuti on kasutajal võimalus enda broneering kustutada, kuid et tegu oleks turvalisema kasutuskogemusega, siis saab broneeringut kustutada vaid broneerimisel kasutatud nime abil, mida kalendris kõikidele kasutajatele ei kuvata. Kõik broneeringud salvestatakse MySQL andmebaasi.

## Kasutusjuhend

Esmalt tuleb allalaadida kõik failid, mis GitLabis on. Ning seejärel kontrollida, et tööks vajalikud lisapakid olemas on:

MySQL-i tööks on vaja installida pythonile lisapakk käsureal `python -m pip install mysql-connector-python`

Veebi osa tööks on vajalik Flaski installimine `python -m pip install Flask` ja `python -m pip install flask-cors`

Programmi töö alustamiseks tuleb käivitada app.py. Kui programm töötab, mine edasi leheküljele http://127.0.0.1:5000/

Broneerimiseks tuleb avanenud aknast valida ruum, kuupäev ja kellaaeg ning sisestada enda nimi, et broneering kinnitada, tuleb vajutada nuppu "Broneeri".
Broneeringu kustutamiseks on nupp "Kustuta", millele klikates avaneb leht loodud broneeringu kustutamiseks. Tuleb sisestada tehtud broneeringu andmed ning sisestada broneerija nimi, seejärel klikates nuppu "Kustuta", tühistatakse broneering.
Broneerimiskalendri all on võimalik näha ruumide ja kuupäevade/kellaaegade lõikes tehtud broneeringuid. Broneeringud on kõikidele nähtavad, kuid broneerijate nimed peidetakse privaatsuse huvides kalendrist. Valides menüüst uue ruumi või tehes muudatusi (broneeringuid lisades või kustutades) vajutada nuppu "Lae andmed" ja muudatused kuvatakse kalendris.

## MySQL andmebaas

* host: mysql.toomas633.com
* port: 3306
* user: test
* paswd: Test-Password01

### Andmebaasi andmete formaat

| kuupäev (yyyy-mm-dd) | alguskell (hh:mm:ss) | lõppkell (hh:mm:ss) | nimi (max 20 märki) |
| --------------------- | -------------------- | -------------------- | -------------------- |

Andmed ruumi kohta loetakse sisse masssiivi "broneering":

_raw:_  `[(datetime.date(2022, 5, 1),), datetime.timedelta(seconds=44100), datetime.timedelta(seconds=49500), 'Toomas Kirsing']`

_puhastatud:_ `broneering[i]`, kus...

- 0 = kuupäev
- 1 = alguskell (sekundites)
- 2 = lõppkell (sekundites)
- 3 = nimi

### Kalendri andmete formaat

Kalendri kirjed muudetakse peale andmebaasist sisse kandmist JSON formaati ning seejärel edastatakse otse kalendrivaate veebilehele.

`<code>`{
  &nbsp;&nbsp; "id": Järjestikune number asukoha kohta loendis (Igal kuupäeval eraldi),
  &nbsp;&nbsp; "title": Ruumi number (nt. A101),
  &nbsp;&nbsp; "url": Soovi korral saab sisesta linke millele kasutaja suunatakse broneeringu kirje peale vajutades,
  &nbsp;&nbsp; "class": event-info (Mis sorti kirjega on tegu, puhtalt kujunduse jaoks),
  &nbsp;&nbsp; "start": Alguskuupäev ja aeg UNIX aja formaadis,
  &nbsp;&nbsp; "end": Lõppkuupäev ja aeg UNIX aja formaadis,
  &nbsp;&nbsp; "time": Kellaaeg kalendris kuvamiseks (nt 10:15-11:45),
  &nbsp;&nbsp; "nimi": Broeerija nimi
}`<code>`
