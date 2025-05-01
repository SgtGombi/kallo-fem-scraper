from flask import Flask, jsonify
import subprocess, json, os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Scraper API működik!'

@app.route('/scrape')
def scrape():
    output_file = 'result.json'
    # Futtatjuk a spidert, és JSON-be irányítjuk az eredményt
    cmd = ['scrapy', 'crawl', 'termekek', '-o', output_file]
    proc = subprocess.run(cmd, cwd=os.getcwd(), capture_output=True, text=True)
    if proc.returncode != 0:
        # Ha hiba van, HTTP 500-at adunk vissza a stderr-rel
        return jsonify({'error': proc.stderr}), 500
    # Beolvassuk a JSON-t és visszaadjuk
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    # A Render a PORT környezeti változóból indítja
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))