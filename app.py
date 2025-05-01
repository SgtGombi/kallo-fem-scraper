from flask import Flask, jsonify
import subprocess
import os
import json
from pathlib import Path

app = Flask(__name__)

# Projekt gyökérkönyvtárának meghatározása
PROJECT_ROOT = Path(__file__).parent.resolve()
SCRAPY_PROJECT_DIR = PROJECT_ROOT / "kallofem_scraper"  # A Scrapy projekt mappája


@app.route('/')
def home():
    return 'Scraper API működik!'


@app.route('/scrape')
def scrape():
    output_file = 'result.json'
    output_path = SCRAPY_PROJECT_DIR / output_file

    # Töröljük a korábbi eredményfájlt, ha létezik
    if output_path.exists():
        output_path.unlink()

    # Scrapy parancs összeállítása
    cmd = [
        'scrapy',
        'crawl',
        'termekek',
        '-o', str(output_path),
        '-t', 'json'
    ]

    try:
        # Scrapy futtatása a projekt mappában
        result = subprocess.run(
            cmd,
            cwd=SCRAPY_PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=300  # 5 perc timeout
        )

        if result.returncode != 0:
            error_msg = f"Scrapy hiba: {result.stderr}" if result.stderr else "Ismeretlen Scrapy hiba"
            return jsonify({'error': error_msg}), 500

        # Eredmény beolvasása
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({'error': 'Nincs kimeneti fájl', 'scrapy_output': result.stdout}), 500

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'A scrapelés túllépte az időkeretet'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))