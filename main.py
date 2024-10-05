from flask import Flask, render_template, request, jsonify
from utility.cv import cvUtils



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
    
    image = request.files['image'] # gets raw image from form data

    if image.filename == '':
        return jsonify({
            'error': "Image wasn't selected!"
            }), 400


    # returns data from the image for pre-filling
    processedImageData = cvUtils.getImageData(image) 
    
    if processedImageData == None: # if processing fails somehow
        return jsonify({
            'error': "The image is not clear! Please use good lighting"
            }), 400

    return jsonify(processedImageData), 200


if __name__ == "__main__":
    app.run(debug = True, host = "127.0.0.1", port= 4321)
