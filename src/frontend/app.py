from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

INFERENCE_URL = "http://inference:8501/predict"

@app.route("/upload", methods=["POST"])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']
    files = {'image': (image.filename, image.read(), image.content_type)}

    # 调用推理服务
    response = requests.post(INFERENCE_URL, files=files)
    if response.status_code != 200:
        return jsonify({"error": "Inference failed"}), 500

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
