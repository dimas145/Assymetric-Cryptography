from flask import Flask, render_template, request, send_from_directory
import os
import re

import algorithms

STATIC_DIR = os.path.abspath("static")

app = Flask(__name__, static_folder=STATIC_DIR)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
                               "img/favicon.ico",
                               mimetype="image/vnd.microsoft.icon")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate-key-page")
def generate_key_page():
    return render_template("generate_key.html", title='Generate Key')


@app.route("/key-form", methods=["POST"])
def key_form():
    if request.method == "POST":
        algorithm_id = request.form["algorithm_id"]
        return render_template("key_form/form" + str(algorithm_id) + ".html")


@app.route("/form", methods=["POST"])
def form():
    if request.method == "POST":
        algorithm_id = request.form["algorithm_id"]
        return render_template("form/form" + str(algorithm_id) + ".html")


@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        text = request.form["text"]
        keys = request.form["keys"]
        command = request.form["command"]
        type = request.form["type"]
        alphabets = re.sub(r'[^a-zA-Z]', '', text).upper()

        # TODO
        if (type == "1"):
            return algorithms.RSA().execute(command, text, keys)
        else:
            return keys + " " + command + " " + type + " " + alphabets


@app.route("/generate-keys", methods=["POST"])
def generate_keys():
    if request.method == "POST":
        keys = request.form["keys"]
        type = request.form["type"]

        # TODO
        if (type == "1"):
            n, e, d = algorithms.RSA().generate_keys(keys)
            return str(n) + " " + str(e) + " " + str(d)
        elif (type == "3"):
            g, n, lamb, mu = algorithms.Paillier().generate_keys(keys)
            return str(g) + " " + str(n) + " " + str(lamb) + " " + str(mu)
        else:
            return keys


@app.route("/action", methods=["POST"])
def action():
    if request.method == "POST":
        state = request.form["state"]
        return "State : " + state


if __name__ == "__main__":
    app.run()
