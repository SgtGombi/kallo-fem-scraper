from flask import Flask
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

app = Flask(__name__)

@app.route("/")
def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl("termekek")  # Spider neve
    process.start()
    return "Spider lefutott!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))