from werkzeug.utils import secure_filename
from flask import Flask, request
from flask_cors import CORS
import json
import os
from pathlib import Path
import numpy as np
from pdf import get_sections, PDF_SOURCE_DIR
from vectorization import vectorize_sections, model
from sentence_transformers import util

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def process(query: str):
    question_enc = model.encode(query)
    similarity = util.cos_sim(encodings, question_enc).numpy().squeeze(axis=1)
    top = np.flip(np.argsort(similarity))[0]

    return {"response": sections[top]}


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
    file = next(Path(PDF_SOURCE_DIR).iterdir())
    sections = np.array(get_sections(file))
    encodings = vectorize_sections(sections)

    app.run(host="0.0.0.0", debug=True)
