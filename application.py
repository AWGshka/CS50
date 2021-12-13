from flask import Flask, render_template, request, redirect
from cs50 import SQL
import sqlite3
import validators
import string


app = Flask(__name__)
db = SQL("sqlite:///database.db")

@app.route("/")
def index():
    return render_template("register.html")

@app.route("/None")
def none():
    return redirect("/")

@app.route("/shorted")
def shorted():
    code = request.args.get("code")
    if not code:
        return redirect("/None")
    else:
        url = db.execute("SELECT url FROM links WHERE code=:code", code=code)
        if not url:
            return redirect("/None")
        else:
            for char in string.punctuation:
                url = str(url)
                url = url.replace("[", '')
                url = url.replace("]", '')
                url = url.replace("'url':", '')
                url = url.replace("{ '", '')
                url = url.replace("'}", '')
            return render_template("/shorted.html", code=code, url=url)

@app.route("/database")
def database():
    rows = db.execute("SELECT * FROM links")
    return render_template("/database.html", rows=rows)

@app.route("/register", methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template("/register.html")
    else:
        code = request.form.get("code")
        url = request.form.get("url")
        valid = validators.url(url)
        sqlitedb = sqlite3.connect('database.db')
        c = sqlitedb.cursor()
        c.execute("SELECT * FROM links WHERE code = '" + code + "'")
        if not code:
            return render_template("/error.html", message="Code is empty.")
        if valid == True:
            if len(c.fetchall()) > 0:
                return render_template("/error.html", message="Code '" + code + "' alredy exists.")
            else:
                db.execute("INSERT INTO links (code, url) VALUES (:code, :url)", code=code, url=url)
                return render_template("/ready.html", code=code)
        else:
            return render_template("/error.html", message="Url provided is not valid.")
