from flask import Flask, send_file
import subprocess

app = Flask(__name__)

@app.route("/")
def get_json():
    subprocess.run(["scrapy", "crawl", "termekek", "-O", "output.json"])  # Spider futtatása
    return send_file("output.json")  # JSON visszaadása

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)