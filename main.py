from flask import Flask, render_template, \
                    session, request, jsonify
import cv2
import numpy as np

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


@app.route("/processImg", methods  = ["POST"]) # image processing
def processImage():
    if 'image' not in request.files:
        return jsonify({
            'error': "Image wasn't recieved!"
            }), 400
    
    image = request.files['image']

    if image.filename == '':
        return jsonify({
            'error': "Image wasn't selected!"
            }), 400

    # add image processing
    imgBytes = np.frombuffer(image.read(), np.uint8)

    imgArr = cv2.imdecode(imgBytes, cv2.IMREAD_COLOR)

    cv2.imshow('test',imgArr) # for verifying that it got uploaded
                              # will remove later

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # dummy data, replace with actual data later
    return jsonify({
        "age": 20,
        "gender": "Male",
        "ethnicity": "Indian",
        "skinTone": "Light brown",
        "sHRI": 1.66,
        "wHRI": 0.17
    }), 200


if __name__ == "__main__":
    app.run(debug = True, host = "127.0.0.1", port= 4321)
