from flask import Blueprint, request, jsonify
import tempfile
import os

from app.resume_parser import extract_text
from app.prompt_builder import build_prompt
from app.llm_client import analyze_resume

api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running"})


@api.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        text = extract_text(tmp_path)

        if not text.strip():
            return jsonify({"error": "Failed to extract text"}), 400

        prompt = build_prompt(text)

        result = analyze_resume(prompt)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if "tmp_path" in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)