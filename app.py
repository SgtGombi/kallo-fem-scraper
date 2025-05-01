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
    output_file = 'result.json'
    cmd = ['scrapy', 'crawl', 'termekek', '-o', output_file, '-t', 'json']
    proc = subprocess.run(cmd, cwd=os.getcwd(), capture_output=True, text=True)

    if proc.returncode != 0:
        return jsonify({'error': proc.stderr}), 500

    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))