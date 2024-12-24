FROM alpine:latest

# 安装glibc
RUN apk --no-cache add \
    libc6-compat

WORKDIR /app
COPY frontend-go .
RUN chmod +x /app/frontend-go
EXPOSE 6999

CMD ["./frontend-go"]
