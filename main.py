from flask import Flask, render_template, \
                    redirect, url_for, session, request
import time



app = Flask(__name__)

keys = open(".keys") # reading secret key
app.secret_key = keys.readline().strip()


@app.route("/") # Home page
def index():
    return render_template("index.html")


@app.route("/createProfile") # for setting up new profile
def createProfile():
    return render_template("signUp.html", mode = "Creation")


@app.route("/updateProfile") # for updating already existing profile
def updateProfile():
    return render_template("signUp.html", mode = "Updation")


@app.route("/chat") # LLM chat page
def chatPage():
    return render_template("chat.html")


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port= 4321)
