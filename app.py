from flask import Flask, jsonify
import subprocess
import os
import json

app = Flask(__name__)


@app.route('/')
def home():
    return 'Scraper API működik!'


@app.route('/scrape')
def scrape():
    output_file = '/tmp/result.json'  # Render.io-n csak /tmp mappába írhatunk

    # Scrapy futtatása JSON formátumban
    cmd = ['scrapy', 'crawl', 'termekek', '-o', output_file, '-t', 'json']
    proc = subprocess.run(cmd, cwd=os.getcwd(), capture_output=True, text=True)

    if proc.returncode != 0:
        return jsonify({'error': proc.stderr}), 500

    # JSON beolvasása, csak az első JSON tömb megnyitása (hibaellenőrzéssel)
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            first_json_array_start = content.find('[')
            first_json_array_end = content.rfind(']') + 1
            json_str = content[first_json_array_start:first_json_array_end]
            data = json.loads(json_str)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))