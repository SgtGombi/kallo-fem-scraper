from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def run_spider():
    result = subprocess.run(
        ['scrapy', 'crawl', 'termekek'],
        cwd='kallofem_scraper',
        capture_output=True,
        text=True
    )
    return f"<pre>{result.stdout or result.stderr}</pre>"

if __name__ == '__main__':
    app.run()
