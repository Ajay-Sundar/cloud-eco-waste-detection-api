import base64
import os
from locust import HttpUser, task, between

IMAGE_PATH = os.path.join("test_images", "benchmark_sample.jpg")


def load_base64_image() -> str:
    with open(IMAGE_PATH, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


class CloudEcoUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.encoded_image = load_base64_image()

    @task(3)
    def predict(self):
        payload = {
            "uuid": "locust-predict",
            "image": self.encoded_image
        }

        with self.client.post(
            "/api/predict",
            json=payload,
            catch_response=True,
            name="/api/predict"
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            try:
                data = response.json()
            except Exception as e:
                response.failure(f"Invalid JSON: {e}")
                return

            required_keys = [
                "uuid",
                "count",
                "detections",
                "boxes",
                "speed_preprocess_ms",
                "speed_inference_ms",
                "speed_postprocess_ms",
            ]

            missing = [k for k in required_keys if k not in data]
            if missing:
                response.failure(f"Missing keys: {missing}")
                return

            response.success()

    @task(1)
    def annotate(self):
        payload = {
            "uuid": "locust-annotate",
            "image": self.encoded_image
        }

        with self.client.post(
            "/api/annotate",
            json=payload,
            catch_response=True,
            name="/api/annotate"
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return

            try:
                data = response.json()
            except Exception as e:
                response.failure(f"Invalid JSON: {e}")
                return

            required_keys = ["uuid", "image"]
            missing = [k for k in required_keys if k not in data]
            if missing:
                response.failure(f"Missing keys: {missing}")
                return

            if not data["image"]:
                response.failure("Annotated image is empty")
                return

            response.success()