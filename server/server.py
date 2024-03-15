from werkzeug.utils import secure_filename
from flask import Flask, request
import json
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def process(query):
    return {"response": query}


@app.route("/submit", methods=["POST"])
def submit():
    if request.method != "POST":
        return
    data = json.loads(request.data.decode())
    return process(data["query"])


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return {"error": "Invalid or missing file uploaded"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"error": "Invalid or missing file uploaded"}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return {"response": f'File "{filename}" uploaded successfully'}
    else:
        return {"error": "File extension not allowed. Please upload a PDF file."}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
