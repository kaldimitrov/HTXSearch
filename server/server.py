from werkzeug.utils import secure_filename

from flask import Flask, request, Response
from flask_cors import CORS

import numpy as np

import chromadb
from chromadb.utils import embedding_functions

import json
import os
from pathlib import Path

from pdf import get_sections, PDF_SOURCE_DIR, render_page
from sentence_transformers import util
from db import ChromaDbInstance

app = Flask(__name__)
CORS(app)

app.chroma = ChromaDbInstance()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/submit", methods=["POST"])
def submit():
    if request.method != "POST":
        return

    data = json.loads(request.data.decode())
    query = data["query"]

    result = app.chroma.query(query)

    return {"response": result}


@app.route("/pages/<file>/<page>", methods=["GET"])
def get_page(file, page):
    if request.method != "GET":
        return

    return Response(render_page(Path(PDF_SOURCE_DIR)/file, page), mimetype='image/png')


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return {"error": "Invalid or missing file uploaded"}, 400

    file = request.files["file"]

    if file.filename == "":
        return {"error": "Invalid or missing file uploaded"}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        file_path = Path(app.config["UPLOAD_FOLDER"]).joinpath(filename)
        file.save(str(file_path))
        app.chroma.vectorize(file_path)
        # file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return {"response": f'File "{filename}" uploaded successfully'}
    else:
        return {"error": "File extension not allowed. Please upload a PDF file."}, 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
