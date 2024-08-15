from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):
    @task
    def complete_task(self):
        self.client.post("/game/complete-task/")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)  # Время ожидания между запросами от одного пользователя
