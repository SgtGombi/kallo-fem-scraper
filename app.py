from flask import Flask, jsonify
import subprocess
import os
import json  # Hozzáadva a JSON fájl olvasásához

app = Flask(__name__)


@app.route('/')
def home():
    return 'Scraper API működik!'


@app.route('/scrape')
def scrape():
    output_file = 'result.json'  # Az adatokat itt fogjuk elmenteni
    # Futtatjuk a scrapy parancsot, hogy JSON-be irányítsuk az eredményt
    cmd = ['scrapy', 'crawl', 'termekek', '-o', output_file]
    proc = subprocess.run(cmd, cwd=os.getcwd(), capture_output=True, text=True)

    # Ellenőrizzük, hogy sikerült-e
    if proc.returncode != 0:
        return jsonify({'error': proc.stderr}), 500

    # Beolvassuk a JSON fájlt és visszaadjuk
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))