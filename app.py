from flask import Flask, render_template, request, send_from_directory
import os
import re
import urllib.parse

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
        elif (type == "2"):
            text = urllib.parse.unquote(text)
            keys = urllib.parse.unquote(keys)
            machine = algorithms.ElGamalMachine()
            print("text")
            print(text)
            print("keys")
            print(keys)
            if (command == "encrypt"):
                return machine.encrypt_full(text, keys)
            else:
                return machine.decrypt_full(text, keys)
        elif (type == "3"):
            print(request.form["r"])
            test = algorithms.Paillier().execute(command, text, keys, int(request.form["r"]))
            return str(test)
        elif (type == "4"):
            text = urllib.parse.unquote(text)
            keys = urllib.parse.unquote(keys)
            print("text")
            print(text)
            print("keys")
            print(keys)
            machine = algorithms.ECCElGamalMachine()
            if (command == "encrypt"):
                return machine.encrypt_full(text, keys)
            else:
                return machine.decrypt_full(text, keys)
        else:
            return keys + " " + command + " " + type + " " + alphabets


@app.route("/generate-keys", methods=["POST"])
def generate_keys():
    if request.method == "POST":
        keys = request.form["keys"]
        type = request.form["type"]
        bit = request.form["bit"]

        # TODO
        if (type == "1"):
            n, e, d = algorithms.RSA().generate_keys(keys)
            return str(n) + " " + str(e) + " " + str(d)
        elif (type == "2"):
            machine = algorithms.ElGamalMachine()

            public_key, private_key = machine.create_key(int(bit))
            return public_key + " " + private_key
        elif (type == "3"):
            g, n, lamb, mu = algorithms.Paillier().generate_keys(keys)
            return str(g) + " " + str(n) + " " + str(lamb) + " " + str(mu)
        elif (type == "4"):
            machine = algorithms.ECCElGamalMachine()
            pub_key, pri_key = machine.create_key_full(int(bit))
            return pub_key + " " + pri_key
        else:
            return keys


if __name__ == "__main__":
    app.run(debug=True)
