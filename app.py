from flask import Flask, send_file
import subprocess
"""
Egyszerű Python script, amely Flask segítségével, subprocess.run parancs segítségével meghívja
 a scraper műküdését, amelynek az eredménye egy .JSON fájl, amit visszaad megjelenítésre. "/" által a Rener
 által adott URL megnyitására a futás eredményét oda adja vissza.
 FONTOS: A RENDER ingyenes verziója erősen csökkentett teljesítményű, a teszthez ajánlom a lokális futtatást.
 Részletek: README.MD
"""
app = Flask(__name__)

@app.route("/") # URL főoldalán fut rögtön a / miatt
def get_json():
    subprocess.run(["scrapy", "crawl", "termekek", "-O", "output.json"])  # Spider futtatása a web megnyitásakor
    return send_file("output.json")  # JSON fájl visszaadása megjelenítésre

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)