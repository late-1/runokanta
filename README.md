# Runokanta

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sovellukseen. 
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan runoja.
* Käyttäjä pystyy lisäämään kuvia visuaalisen runon esitykseen.
* Käyttäjä näkee sovellukseen lisätyt runot.
* Käyttäjä pystyy hakemaan runoja hakusanalla.
* Käyttäjä pystyy arvostelemaan ja arvioimaan muiden runoja. 
* Sovelluksessa on käyttjäsivut, jotka näyttävät käyttäjän lisäämät runot ja arvostelut.
* Käyttäjä pystyy valitsemaan runolle yhden tai useamman luokittelun (esim. haiku, lyriikka tai balladi)
* Käyttäjä pystyy lisäämään runolle yhden tai useamman aihealueen / teeman (esim. kaiho, kaipuu, katkeruus tai ilo)

## Sovelluksen asennus 

Sovellus testattu ja kehitetty python 3.10.19 versiolle

Asenna `flask`–kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot: 
```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```
