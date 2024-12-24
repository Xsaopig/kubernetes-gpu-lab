package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

const INFERENCE_URL = "http://localhost:8501/predict"

// const INFERENCE_URL = "http://inference:8501/predict"

// 上传文件的 handler
func upload(c *gin.Context) {
	// 获取上传的文件
	file, _ := c.FormFile("image")
	if file == nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "No image uploaded"})
		return
	}

	// 打开文件
	src, err := file.Open()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to open file"})
		return
	}
	defer src.Close()

	// 读取文件内容
	fileBytes, err := io.ReadAll(src)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read file"})
		return
	}

	// 构建请求体
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)
	part, err := writer.CreateFormFile("image", file.Filename)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create form file"})
		return
	}

	// 写入文件内容
	_, err = part.Write(fileBytes)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to write file content"})
		return
	}

	// 关闭 writer
	err = writer.Close()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to close writer"})
		return
	}

	// 调用推理服务
	resp, err := http.Post(INFERENCE_URL, writer.FormDataContentType(), body)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to call inference service"})
		return
	}
	defer resp.Body.Close()

	// 如果推理服务调用失败，返回错误
	if resp.StatusCode != http.StatusOK {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Inference failed"})
		return
	}

	// 解析推理服务的响应
	var result map[string]interface{}
	err = json.NewDecoder(resp.Body).Decode(&result)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to parse response"})
		return
	}

	// 返回推理结果
	c.JSON(http.StatusOK, result)
}

func main() {
	// 创建 gin 路由
	r := gin.Default()

	// 定义路由，上传文件
	r.POST("/upload", upload)

	// 启动服务
	err := r.Run(":6999")
	if err != nil {
		fmt.Println("Failed to start the server:", err)
		os.Exit(1)
	}
}
