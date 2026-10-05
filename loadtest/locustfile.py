"""Chạy: locust -f loadtest/locustfile.py --headless -u 50 -r 10 -t 60s --host http://localhost:8000
Nên chạy server với OCR_ENGINE=mock để đo kiến trúc chứ không đo Gemini."""
import base64
import uuid

from locust import HttpUser, between, task

PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/q842iQAAAABJRU5ErkJggg==")


class Student(HttpUser):
    wait_time = between(0.5, 1.5)

    def on_start(self):
        name, pw = f"u{uuid.uuid4().hex[:10]}", "matkhau123"
        self.client.post("/auth/register", json={"username": name, "password": pw})
        token = self.client.post("/auth/login", json={"username": name, "password": pw}).json()["access_token"]
        self.headers = {"Authorization": f"Bearer {token}"}
        self.assignment_id = self.client.post("/assignments", headers=self.headers, json={
            "title": "PT bậc nhất", "question": "2x+4=12", "correct_answer": "4"}).json()["id"]

    @task(5)
    def list_assignments(self):
        self.client.get("/assignments")

    @task(3)
    def submit(self):
        self.client.post("/submissions", headers=self.headers, data={"assignment_id": self.assignment_id},
                         files={"file": ("bai.png", PNG, "image/png")})

    @task(2)
    def my_submissions(self):
        self.client.get("/submissions", headers=self.headers)
