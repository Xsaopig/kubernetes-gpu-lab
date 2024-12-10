#!/bin/bash

# 工作负载文件列表
workloads=("workloadtest.py")

# 无限循环
while true; do
    for workload in "${workloads[@]}"; do
        echo "正在运行 ${workload}..."
        
        # 运行 locust 命令
        locust -f "$workload" --host http://127.0.0.1:31157 --csv stats --only-summary --autostart --reset-stats --autoquit 1
        
        # 记录 locust 进程的 PID
        locust_pid=$!
        
        # 等待 locust 进程结束
        wait $locust_pid
        
        # 可选：在两个测试之间等待一段时间
        # sleep 60 # 例如，等待60秒
    done
done
