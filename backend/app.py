# backend/app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
from werkzeug.utils import secure_filename
from models.legal_simplifier import (
    summarize_document,
    extract_clauses,
    answer_question,
    translate_text,
    synthesize_speech
)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

# Simple in-memory "database" for demo
DOC_STORE = {}

@app.route("/")
def index():
    return jsonify({"message": "LexiGen AI Backend Running"}), 200

@app.route("/api/v1/upload", methods=["POST"])
def upload_document():
    """
    Accepts file upload (PDF/DOCX/TXT). Saves file and returns doc_id.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    f = request.files['file']
    if f.filename == "":
        return jsonify({"error": "No selected file"}), 400
    filename = secure_filename(f.filename)
    doc_id = str(uuid.uuid4())
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{doc_id}_{filename}")
    f.save(saved_path)

    # For demo: read text if txt, else placeholder
    if filename.lower().endswith(".txt"):
        with open(saved_path, "r", encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = f"[Sample extracted text from {filename}. Replace with Document AI OCR in production.]"

    DOC_STORE[doc_id] = {"filename": filename, "path": saved_path, "text": text}
    return jsonify({"doc_id": doc_id, "filename": filename}), 200

@app.route("/api/v1/summary/<doc_id>", methods=["GET"])
def get_summary(doc_id):
    doc = DOC_STORE.get(doc_id)
    if not doc:
        return jsonify({"error": "doc not found"}), 404
    summary = summarize_document(doc["text"])
    return jsonify({"doc_id": doc_id, "summary": summary}), 200

@app.route("/api/v1/clauses/<doc_id>", methods=["GET"])
def get_clauses(doc_id):
    doc = DOC_STORE.get(doc_id)
    if not doc:
        return jsonify({"error": "doc not found"}), 404
    clauses = extract_clauses(doc["text"])
    return jsonify({"doc_id": doc_id, "clauses": clauses}), 200

@app.route("/api/v1/qa", methods=["POST"])
def qa():
    data = request.json or {}
    doc_id = data.get("doc_id")
    query = data.get("query", "")
    if not doc_id or not query:
        return jsonify({"error": "doc_id and query required"}), 400
    doc = DOC_STORE.get(doc_id)
    if not doc:
        return jsonify({"error": "doc not found"}), 404
    answer = answer_question(doc["text"], query)
    return jsonify({"doc_id": doc_id, "query": query, "answer": answer}), 200

@app.route("/api/v1/translate", methods=["POST"])
def translate():
    data = request.json or {}
    doc_id = data.get("doc_id")
    language = data.get("language", "hi")  # default hindi for demo
    if not doc_id:
        return jsonify({"error": "doc_id required"}), 400
    doc = DOC_STORE.get(doc_id)
    if not doc:
        return jsonify({"error": "doc not found"}), 404
    translated = translate_text(doc["text"], language)
    return jsonify({"doc_id": doc_id, "language": language, "translated": translated}), 200

@app.route("/api/v1/audio/<doc_id>", methods=["GET"])
def audio(doc_id):
    """Return an mp3 URL or file - this demo synthesizes a file and returns path"""
    doc = DOC_STORE.get(doc_id)
    if not doc:
        return jsonify({"error": "doc not found"}), 404
    text = summarize_document(doc["text"])
    audio_path = synthesize_speech(text, doc_id)
    return send_file(audio_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
