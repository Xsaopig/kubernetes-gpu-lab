#!/bin/bash

# 设置要上传的图像路径
IMAGE_PATH="/data/zhx/kubernetes-gpu-lab/data/bus.jpg"
# 设置目标 URL
URL="http://127.0.0.1:31157/upload"

# 循环发送请求
while true; do
  curl -X POST -F "image=@${IMAGE_PATH}" ${URL}
  # 等待一秒后继续执行
#   sleep 1
done
