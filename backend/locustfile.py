from locust import HttpUser, task, between, TaskSet

class UserBehavior(TaskSet):

    # def on_start(self):
    #     # Endpoint logowania
    #     login_url = "/auth/login/"
    #     # Dane logowania
    #     email = "admin@admin.com"
    #     password = "Test.Test.1"

    #     data = {"email": email, "password": password}
        
    #     # Wysłanie żądania logowania z Basic Auth
    #     response = self.client.post(login_url, json=data)
    #     if response.status_code == 200:
    #         print("Login status", response.status_code)
    #         print("Login successful")
    #         print("Token:", response.json().get("access_token"))
    #         self.token = response.json().get("access_token")
    #     else:
    #         print("Login status", response.status_code)
    #         print("Login failed:", response.text)
    #         self.token = None

    @task
    def vehicles_page(self):
        # headers = {"Authorization": f"Bearer {self.token}"}
        headers = {}
        self.client.get("/vehicles/", headers=headers)

    @task
    def users_page(self):
        # headers = {"Authorization": f"Bearer {self.token}"}
        headers = {}
        self.client.get("/users/", headers=headers)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)