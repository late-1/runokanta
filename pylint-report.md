# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta 

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:43:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:48:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:61:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:83:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:100:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:106:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:160:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:179:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:195:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:227:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:247:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:258:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:280:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:294:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:305:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module poems
poems.py:1:0: C0114: Missing module docstring (missing-module-docstring)
poems.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:50:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:60:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:72:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:82:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:87:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:92:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:97:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:108:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:114:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:130:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:142:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:147:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:152:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:157:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:163:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:169:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:215:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:220:0: C0116: Missing function or method docstring (missing-function-docstring)
poems.py:226:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:31:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 8.32/10 (previous run: 8.30/10, +0.03)
```

Käydään läpi raportin sisältö ja perustellaan miksi kyseisiä asioita ei ole korjattu. 

## Docstring-ilmoitukset

Suurin osa pylintin ilmoituksista ovat seuraavanlaisia:
```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
```
Nämä kertovat siitä, että moduuleista puuttuu dokumentointi ja kommentointi. Sovellusta kehittäessä on päätetty, että funktioita tai moduuleita ei kommentoida.

## Vaarallinen oletusarvo

Raportissa on seuraavanlaiset ilmoitukset:
```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Rivin ```20``` ilmoitus koskee seuraavaa:

```
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```

Ilmoitus viittaa ```db.py``` moduulin funktioiden ```execute``` ja ```query``` parametreihin ```params```, jonka oletusarvoksi on asetettu tyhjä lista ```[]```

Tässä tapauksessa vaarallinen oletusarvo ei haittaa, koska ```sqlite3``` -kirjaston ```execute``` metodi lukee listaa, eikä muuta sitä. Python alustaa oletusarvot vain kerran. Jos listaa muokattaisiin funktion sisällä, muutos jäisi pysyvästi muistiin ja sotkisi kaikki seuraavat kutsukerrat.

## Tarpeeton else

Raportissa on seuraava ilmoitus liittyen turhaan ```else``` ehtorakenteeseen.
```
users.py:31:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
```
ilmoitus viittaa seuraavaan koodinpätkään:
```
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None
```
Tämän saman voisi kirjoittaa tiiviimmin:
```
    if check_password_hash(password_hash, password):
        return user_id
    return None
```
Mutta tässä tapauksessa kehittäjän mielestä on selkeämpää säilyttää ```else```luettavuuden ja selkeyden vuoksi. Onnistunut kirjautuminen palauttaa käyttäjälle tunnisteen (```user_id```), kun taas epäonnistunut palauttaa arvon ```None```. 


## Vakion nimi

Raportissa on seuraava ilmoitus liittyen vakion nimeen:
```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```
Tässä määritelty muuttuja tulkitaan vakioksi, jonka nimen tulisi olla tyyliohjeiden mukaan kirjoitettu suurilla kirjaimilla, eli ```SECRET_KEY```. Kehittäjän mielestä tässä tilanteessa näyttää paremmalta jos muuttujan nimi on kirjoitettu pienillä kirjaimilla. 