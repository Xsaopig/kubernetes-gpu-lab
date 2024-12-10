import random
from locust import HttpUser, LoadTestShape, TaskSet, constant, task , events

class UserTasks(TaskSet):
    @task
    def upload_image(self):
        # 指定文件路径
        file_path = "/data/zhx/kubernetes-gpu-lab/data/bus.jpg"
        # 打开文件并发送 POST 请求
        with open(file_path, "rb") as image_file:
            files = {"image": image_file}
            response = self.client.post("/upload", files=files)
            # 可选：记录响应内容
            if response.status_code != 200:
                print(f"Upload failed: {response.status_code}, {response.text}")

class WebsiteUser(HttpUser):
    wait_time = constant(0.5)
    tasks = [UserTasks]

class StagesShapeWithCustomUsers(LoadTestShape):
    stages = [
        {"duration": 300, "users": 10, "spawn_rate": 1},
        # {"duration": 300, "users": 200, "spawn_rate": 10},
        # {"duration": 300, "users": 50, "spawn_rate": 10},
        # {"duration": 300000, "users": 100, "spawn_rate": 50},
    ]
    
    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                try:
                    tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                except:
                    tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None