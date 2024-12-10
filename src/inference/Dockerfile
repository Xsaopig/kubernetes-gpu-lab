# 使用更轻量的 python:3.9-slim 镜像
FROM python:3.9-slim

# 安装必要的系统依赖，包括 glib 和 opencv 所需的库
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    && apt-get clean

# 安装支持 CUDA 12.1 的 PyTorch 及其他依赖
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu121

# 安装其他依赖，包括 ultralytics 和 flask
RUN pip install --no-cache-dir \
    ultralytics flask pillow

# 官方依赖
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制模型和代码
WORKDIR /app
COPY models/ ./models
COPY app.py ./app.py

# 使用更轻量的模型（YOLOv5n）
RUN wget https://github.com/ultralytics/yolov5/releases/download/v6.0/yolov5n.pt -P ./models

# 启动 Flask 服务
CMD ["python", "app.py"]
