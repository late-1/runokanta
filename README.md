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

## Tietokannan toiminta suurella tietomäärällä

Testiä varten luodaan ```seed.py``` avulla tietokanta, jossa on seuraavat parametrit:
```
user_count = 10000
poem_count = 10**6
review_count = 10**7
```
Koodi luo tietokannan, jossa on 10 000 käyttäjää, 1 000 000 runoa ja 10 000 000 arvostelua. 

Testit tehtiin skeemalla joka on indeksöity sekä skeemalla joka ei ole. 

Latausnopeuksia mitattiin seuraavanlaisesti:

1. luodaan tunnus
2. kirjaudutaan sisään
3. kirjoitetaan uusi runo (```poem/1000001```)
4. mennään runoon numero ```100 000```, ```500 000``` ja ```1 000 000```.
5. mennään käyttäjään: ```5 000``` ja ```10 000```
6. haetaan hausta hakusanalla ```sisältö```, jolloin jokainen runo tulisi latautua kerralla. (full table scan)
7. Etusivu sivu 50000 (keskellä, OFFSET ~499990)
8. . Etusivu sivu 100000 (vanhimmat runot, OFFSET ~999990)

### Ilman indeksejä
```sqlite3 database.db < /schema_no_indexes.sql``` luodaan tietokanta ILMAN indeksejä

```python3 seed.py``` luodaan testitietokanta

Tarkistetaan tietokannan koko:
```
(venv) λ ~/runokanta/ main* ls -lh database.db   
-rw-r--r--@ 1 lauri  staff   489M Dec 11 00:23 database.db
```

Testit:
```
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
elapsed time: 0.22 s
127.0.0.1 - - [11/Dec/2025 01:41:04] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:41:04] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:41:05] "GET /register HTTP/1.1" 200 -
elapsed time: 0.08 s
127.0.0.1 - - [11/Dec/2025 01:41:09] "POST /create HTTP/1.1" 302 -
elapsed time: 0.18 s
127.0.0.1 - - [11/Dec/2025 01:41:09] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:41:12] "GET /login HTTP/1.1" 200 -
elapsed time: 0.08 s
127.0.0.1 - - [11/Dec/2025 01:41:15] "POST /login HTTP/1.1" 302 -
elapsed time: 0.17 s
127.0.0.1 - - [11/Dec/2025 01:41:15] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:41:26] "GET /new_poem HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:41:34] "POST /create_poem HTTP/1.1" 302 -
elapsed time: 0.5 s
127.0.0.1 - - [11/Dec/2025 01:41:34] "GET /poem/1000001 HTTP/1.1" 200 -
elapsed time: 0.5 s
127.0.0.1 - - [11/Dec/2025 01:41:49] "GET /poem/100000 HTTP/1.1" 200 -
elapsed time: 0.6 s
127.0.0.1 - - [11/Dec/2025 01:42:00] "GET /poem/500000 HTTP/1.1" 200 -
elapsed time: 0.49 s
127.0.0.1 - - [11/Dec/2025 01:42:13] "GET /poem/1000000 HTTP/1.1" 200 -
elapsed time: 8.96 s
127.0.0.1 - - [11/Dec/2025 01:42:36] "GET /user/5000 HTTP/1.1" 200 -
elapsed time: 8.78 s
127.0.0.1 - - [11/Dec/2025 01:42:51] "GET /user/10000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:43:02] "GET /find_poem HTTP/1.1" 200 -
elapsed time: 4.1 s
127.0.0.1 - - [11/Dec/2025 01:43:09] "GET /find_poem?query=sisältö HTTP/1.1" 200 -
elapsed time: 0.74 s
127.0.0.1 - - [11/Dec/2025 01:43:52] "GET /50000 HTTP/1.1" 200 -
elapsed time: 0.7 s
127.0.0.1 - - [11/Dec/2025 01:44:06] "GET /100000 HTTP/1.1" 200 -
```

### Indeksien kanssa
```sqlite3 database.db < schema.sql```

```python3 seed.py```luodaan testitietokanta


Tarkistetaan tietokannan koko:
```
(venv) λ ~/runokanta/ main* ls -lh database.db                        
-rw-r--r--@ 1 lauri  staff   649M Dec 11 01:21 database.db
```

Testit:
```
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
elapsed time: 0.02 s
127.0.0.1 - - [11/Dec/2025 01:21:28] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:21:28] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:21:32] "GET /register HTTP/1.1" 200 -
elapsed time: 0.09 s
127.0.0.1 - - [11/Dec/2025 01:21:36] "POST /create HTTP/1.1" 302 -
elapsed time: 0.01 s
127.0.0.1 - - [11/Dec/2025 01:21:36] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:21:38] "GET /login HTTP/1.1" 200 -
elapsed time: 0.07 s
127.0.0.1 - - [11/Dec/2025 01:21:41] "POST /login HTTP/1.1" 302 -
elapsed time: 0.01 s
127.0.0.1 - - [11/Dec/2025 01:21:41] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:21:47] "GET /new_poem HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:21:58] "POST /create_poem HTTP/1.1" 302 -
elapsed time: 0.01 s
127.0.0.1 - - [11/Dec/2025 01:21:58] "GET /poem/1000001 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:22:24] "GET /poem/100000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:22:58] "GET /poem/500000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:23:08] "GET /poem/1000000 HTTP/1.1" 200 -
elapsed time: 0.02 s
127.0.0.1 - - [11/Dec/2025 01:23:23] "GET /user/5000 HTTP/1.1" 200 -
elapsed time: 0.01 s
127.0.0.1 - - [11/Dec/2025 01:23:35] "GET /user/10000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [11/Dec/2025 01:23:42] "GET /find_poem HTTP/1.1" 200 -
elapsed time: 3.94 s
127.0.0.1 - - [11/Dec/2025 01:23:50] "GET /find_poem?query=sisältö HTTP/1.1" 200 -
elapsed time: 0.32 s
127.0.0.1 - - [11/Dec/2025 01:24:09] "GET /50000 HTTP/1.1" 200 -
elapsed time: 0.49 s
127.0.0.1 - - [11/Dec/2025 01:24:31] "GET /100000 HTTP/1.1" 200 -
```
## Johtopäätökset

Indeksien kanssa tietokanta on n. 33% suurempi, mutta toiminnaltaan paljon tehokkaampi ja nopeampi. 

Merkittävimmät parannukset esiintyvät käyttäjäsivuilla.
- Ilman indeksejä: ```8.96s```ja ```8.78s```
- Indeksien kanssa: ```0.02s``` ja ```0.01s```
- Käyttäjäsivut tekee neljä kyselyä:
  * käyttäjän runojen määrä
  * arvosteluiden keskiarvo (```JOIN poems + reviews```)
  * top 3 kategoriaa (```JOIN + GROUP BY```)
  * top 5 teemaa (```JOIN + GROUP BY```)

Indeksin kanssa, käyttäjäsivut latautuivat siis n. 450x nopeammin. Ilman ```ìdx_poems_user_id```SQL skannaa kaikki 1 000 000 runoa jokaisessa kyselyssä. Arvosteluiden keskiarvon laskeminen ilman ```ìdx_reviews_poem_id```skannaa lisäksi kaikki 10 000 000 arvostelua, eli yhteensä yli 11 miljoonaa riviä / käyttäjäsivun lataus.

Runosivut n. 50x nopeampia indeksien kanssa.
- ilman indeksejä ```0.5s - 0.6s```indekseillä ```0.0s - 0.1s```

LIKE-operaatioinen haku ```WHERE content LIKE '%sisältö%'``` ei voi hyödyntää indeksejä koska:
- SQLite joutuu skannaamaan jokaisen runon sisällön
- Wildcard haku (```%sisältö%```) estää indeksin käytön
- Sivun suorituskykyä voisi parantaa sivutuksella, tällä hetkellä selain yrittää näyttää suuren html-sivun kerralla
- Hakua voisi myös rajoittaa ```LIMIT```ja ```OFFSET```:lla, mutta testauksen vuoksi se on koettu tässä turhaksi.


  
## Tulosten yhteenveto
| Toiminto | Ilman indeksejä (s) | Indeksien kanssa (s) |
|----------|---------------------|----------------------|
| Etusivu (/) | 0.22 | 0.02 |
| Tunnuksen luonti | 0.08 | 0.09 |
| Kirjautuminen | 0.08 | 0.07 |
| Uuden runon luonti | 0.00 | 0.00 |
| /poem/100000 | 0.50 | 0.00 |
| /poem/500000 | 0.60 | 0.00 |
| /poem/1000000 | 0.49 | 0.00 |
| /user/5000 | 8.96 | 0.02 |
| /user/10000 | 8.78 | 0.01 |
| ?query=sisältö | 4.10 | 3.94 |
| /50000 | 0.74 | 0.32 |
| /100000 | 0.70 | 0.49 |

