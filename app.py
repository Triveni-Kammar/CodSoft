import io
from flask import Flask, request, render_template, jsonify
from PIL import Image
import torch
from transformers import pipeline

app = Flask(__name__)

device = 0 if torch.cuda.is_available() else -1
captioner = pipeline(
    "image-to-text",
    model="nlpconnect/vit-gpt2-image-captioning",
    device=device
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/caption", methods=["POST"])
def caption():
    if "image" not in request.files:
        return jsonify({"error": "No image file in request"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        return jsonify({"error": f"Cannot open image: {e}"}), 400

    try:
        results = captioner(image)
        if isinstance(results, list) and len(results) > 0:
            result = results[0]
            text = result.get("generated_text") or result.get("caption") or result.get("text") or str(result)
        elif isinstance(results, dict):
            text = results.get("generated_text") or results.get("caption") or str(results)
        else:
            text = str(results)

    except Exception as e:
        return jsonify({"error": f"Inference error: {e}"}), 500

    return jsonify({"caption": text})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
