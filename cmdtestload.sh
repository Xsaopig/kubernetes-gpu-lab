#!/bin/bash

# 设置要上传的图像路径
IMAGE_PATH1="/data/zhx/kubernetes-gpu-lab/data/bus.jpg"
IMAGE_PATH2="/data/zhx/kubernetes-gpu-lab/data/zidane.jpg"
# 设置目标 URL
URL="http://127.0.0.1:6999/upload"

# 循环发送请求
while true; do
  curl -X POST \
   -F "image=@${IMAGE_PATH1}" \
   -F "image=@${IMAGE_PATH2}" \
  ${URL}
  # 等待一秒后继续执行
#   sleep 1
done
