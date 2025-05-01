# KÁLLÓ-Fém Webshop Scraper
# GITHUB LINK: https://github.com/SgtGombi/kallo-fem-scraper
## Projekt feladata:
A KÁLLÓ-Fém webshop /keriteselemek oldal termékeinek kigyűjtése
Scrapy használatával, illetve eseti duplikációellenőrzés a checkduplicates.py által.

## Függőségek:
- Python 3.13
- Beépített modulok: json, collections (defaultdict), sys
- Scrapy 2.12.0

## Futtatás (CMD): 
- cd gyökérkönyvtár/
- scrapy crawl termekek -o outputFajlnev.json

## Duplikátumok eseti ellenőrzése (CMD):
- cd gyökérkönyvtár/
- python checkduplicates.py fajlneve.json

## Fájlstruktúra:
### kallo_fem_scraper/
- spiders/termekek_spider.py -- Fő spider kód
- checkduplicates.py -- Duplikátum ellenőrző
- termekek.json -- Példa kimenet
- README.md -- Dokumentáció

## Spider: termekek_spider.py
#### A webshop tanulmányozása után tett megállapítások:
A webshop alapértelmezett kerítéselemek oldala (https://kallofem.hu/shop/group/keriteselemek)
rendezéssel van ellátva, amely scrapelés során duplikációhoz, adatvesztéshez vezethet.
Ezzel szemben a ?page=1-el való URL kiegészítés értelmezve van, amely már nem rendelkezik rendezéssel.
Emiatt a feldolgozás a "?page=1"-el ellátott URL kiegészítéssel indul, majd automatikus lapozással 
halad végig az oldalakon.
<br><br>
További megállapítás, hogy az oldalak rendezettek, konstans számú elemet jelenítenek meg,
az oldalak között nincs átfedés, és nincs duplikáció.
Emiatt a kódba nem került duplikációellenőrzés, mivel jelen állapotban csak felesleges futást
eredményezne. Eseti ellenőrzés esetére viszont létrejött egy ellenőrző script is, lásd lejjebb.

## Ellenőrzés: checkduplicates.py
Mivel a spiderben a fent leírtak miatt szükségtelen az ellenőrzés, attól még néha nem árt.
Emiatt jött létre ez a script, amely CMD-ben futtatva ellenőrzést végez, szöveges válaszban adja
meg van-e duplikált adat, és melyek azok, vagy nincs. Felhasználóbarát, CMD-ben hibás parancs input
esetén hibaüzenetet is dob.