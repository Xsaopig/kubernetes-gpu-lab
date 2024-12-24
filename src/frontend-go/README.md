go build -o frontend-go
docker build -t frontend-go:v1 ./
docker stop frontend-go
docker rm frontend-go
docker create --name=frontend-go -p 6999:6999 frontend-go:v1
docker start frontend-go