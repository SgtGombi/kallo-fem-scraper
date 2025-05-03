# KÁLLÓ-Fém Webshop Scraper
## GITHUB LINK: https://github.com/SgtGombi/kallo-fem-scraper
## RENDER LINK: https://kallo-fem-scraper.onrender.com/
## 1. Projekt feladata:
A KÁLLÓ-Fém webshop /keriteselemek oldal termékeinek kigyűjtése
Scrapy használatával, illetve eseti duplikációellenőrzés a checkduplicates.py által.

## 2. Függőségek:
- Python 3.13
- Flask
- Scrapy 2.12.0
- Beépített modulok: json, collections (defaultdict), sys
- Egyéb függőségek: requirements.txt

## 3. Lokális futtatás (CMD):
- cd klónozásHelye/
- Repo klónozás: 'git clone https://github.com/SgtGombi/kallo-fem-scraper.git'
- Függőségek telepítése: 'pip install -r requirements.txt'
- Alábbi futtatások a gyökérmappából
### 3.1. Futtatás (CMD):
- scrapy crawl termekek -o outputFajlnev.json
### 3.2 Duplikátumok eseti ellenőrzése (CMD):
- python checkduplicates.py fajlneve.json

## 4. Fájlstruktúra:
### kallo_fem_scraper/
- spiders/termekek_spider.py -- Fő spider kód
- checkduplicates.py -- Duplikátum ellenőrző
- termekek.json -- Példa kimenet
- README.md -- Dokumentáció
- venv/app.py/result.json/requirements.txt/Procfile -- RENDER fájlok
- iSwearItWorks.png -- RENDER futás minta

## 5. Spider: termekek_spider.py
#### A webshop tanulmányozása után tett megállapítások:
A webshop alapértelmezett kerítéselemek oldala (https://kallofem.hu/shop/group/keriteselemek)
rendezéssel van ellátva, amely scrapelés során duplikációhoz, adatvesztéshez vezethet.
Ezzel szemben a ?page=1-el való URL kiegészítés értelmezve van, amely már nem rendelkezik rendezéssel.
Emiatt a feldolgozás a "?page=1"-el ellátott URL kiegészítéssel indul, majd automatikus lapozással 
halad végig az oldalakon.
<br>
További megállapítás, hogy az oldalak page=x esetén összefüggően rendezettek, konstans számú elemet jelenítenek meg oldalanként,
az oldalak között nincs átfedés, és nincs duplikáció.
Emiatt a kódba nem került duplikációellenőrzés, mivel jelen állapotban csak felesleges futást
eredményezne. Eseti ellenőrzés esetére viszont létrejött egy ellenőrző script is, lásd lejjebb.

## 6. Ellenőrzés: checkduplicates.py
Mivel a spiderben a fent leírtak miatt szükségtelen az ellenőrzés, attól még néha nem árt.
Emiatt jött létre ez a script, amely CMD-ben futtatva ellenőrzést végez, szöveges válaszban adja
meg van-e duplikált adat, és melyek azok, vagy nincs. Felhasználóbarát, CMD-ben hibás parancs input
esetén hibaüzenetet is dob.

## 7. Render web service
GitHub repo-ból végzi a deploy-t. Build Command a "pip install -r requirements.txt",
ami telepíti a függőségeket build során, majd a start command: "python app.py",
amely flask segítségével subprocess által lefuttatja a "termekek" nevű spidert, majd a generált fájlt
visszaküldi.

## 8. Render megjegyzés:
A Heroku teljesen fizetőssé vált, a RENDER pedig nagyon gyenge futást eredményez a próba/ingyenes (10% CPU kihasználás, 512mb ram) verzióban. Futást 50mp-nél tovább nem engedélyez, így megtörténhet hogy a komplett scrape nem fut le (mivel a lekért adat jelenleg 1902 elem/68 oldal), így az adat hiányos lesz. A futás körülményei sem egyszerűbbek, ebben a verzióban gyakorlatilag a webservice kikapcsol 15 perc után, és csak manuálisan (render-dashboard belépésre) indul, ami további késedelmeket okozhat, vagy sajnos egyáltalán nem indul.
A futás ellenőrzésre került, aktív állapotban a webservice az "iSwearItWorks.png" képen látható eredményt adja.
### Célszerűbb a projektem tényleges tesztelése a fent leírt módokon.