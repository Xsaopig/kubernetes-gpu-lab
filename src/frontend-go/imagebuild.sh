#!/bin/bash 

go build -o frontend-go
docker build -t frontend-go:latest ./
docker stop frontend-go
docker rm frontend-go
docker create --name=frontend-go -p 6999:6999 frontend-go:latest
docker start frontend-go