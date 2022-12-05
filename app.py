from threading import Thread

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/commands")
def commands():
    return render_template("commands.html", title="Commands")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
