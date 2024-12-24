from flask import Flask, request, jsonify
import torch
from PIL import Image
import io
# from ultralytics import YOLO

app = Flask(__name__)

# 检查是否有可用的 GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

# 加载模型
MODEL_PATH = "./models/yolov5n.pt"
model = torch.hub.load('./yolov5-master', 'custom', source='local', path=MODEL_PATH)
# model = YOLO(MODEL_PATH)
model.to(device)  # 将模型移到 GPU

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image = Image.open(io.BytesIO(image_file.read())).convert('RGB')

    # 执行推理
    results = model(image)

    # 处理推理结果
    detections = results.xyxy[0].tolist()
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
