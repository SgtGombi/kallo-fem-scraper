"""
KÁLLÓ-Fém webshop /keriteselemek termékeinek scrapelése Scrapy használatával

Funkciók:
- Termékadatok kinyerése: név,ár,kép URL
- Automatikus lapozás a bejáráshoz
- Kimenet: .JSON fájl

Példa futtatás a gyökérkönyvtárból:
scrapy crawl termekek -o fajlnev.json
"""

import scrapy

class TermekekSpider(scrapy.Spider):
    #Scrapy spider a termékek kigyűjtésére
    name = "termekek"
    allowed_domains = ["kallofem.hu"]
    start_urls = ["https://kallofem.hu/shop/group/keriteselemek?page=1"]

    """
    A start url nem az alapértelmezett /keriteselemek page, mivel arra rendezés van
    beállítva. Mivel a page=1 értelmezve van, így ezt használva nem lesz duplikátum,
    sem kihagyás, és a kódban duplicate ellenőrzésre sincs szükség ezesetben a webshop
    felépítésének köszönhetően (nincs átfedett oldal, sem duplikált adat).
    """

    def parse(self, response):
        """
        Parse függvény: Feldolgoz, és kinyer adatokat.
        Args: response: scrapy válaszobjektum a letöltött oldallal
        Yield: adatok kiadása kért formátumban
        """
        for product in response.css("div.col-6.col-md-3 article.product-row"): #Adathoz legközelebbi doboz a könyebb kereséshez
            name = product.css("h4::text").get()
            price = product.css(".product-price::text").get()
            image = product.css("img::attr(src)").get()
            # szükséges adatok helyének legpontosabb megadása

            yield {
                "Terméknév": name.strip() if name else None,
                "Ár": price.strip() if price else None,
                "Kép": response.urljoin(image) if image else None,
            } # Dictionary formátum létrehozása, None ha hiányos az adat,JSON-ban null-ként jelenik meg.

        next_page = response.css("a.page-link[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        # begyűjti a következő oldal linkjét, és ha van, akkor visszahívja a következő oldalra a parse függvényt.