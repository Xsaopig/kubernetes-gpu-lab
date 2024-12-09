FROM python:3.9-slim

# 安装依赖
RUN apt-get update && apt-get install -y libgl1 wget
RUN pip install --no-cache-dir torch torchvision ultralytics flask pillow

# 添加模型与代码
WORKDIR /app
COPY models/ ./models
COPY app.py ./app.py

CMD ["python", "app.py"]
