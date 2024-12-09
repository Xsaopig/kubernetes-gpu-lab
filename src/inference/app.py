from flask import Flask, request, jsonify
import torch
from PIL import Image
import io

app = Flask(__name__)

# Load YOLOv5 model
MODEL_PATH = "./models/yolov5s.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH)
model.eval()

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read()))

    # Perform inference
    results = model(image)

    # Process results
    detections = results.xyxy[0].tolist()  # Bounding boxes
    output = []
    for detection in detections:
        x_min, y_min, x_max, y_max, confidence, class_id = detection
        output.append({
            "x_min": int(x_min),
            "y_min": int(y_min),
            "x_max": int(x_max),
            "y_max": int(y_max),
            "confidence": float(confidence),
            "class_id": int(class_id),
            "label": model.names[int(class_id)]
        })

    return jsonify({"detections": output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501)
