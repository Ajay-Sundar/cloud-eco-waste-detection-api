# CloudEco Waste Detection API

CloudEco is a cloud-native computer vision API for detecting plastic and waste objects in images. It exposes a FastAPI service backed by a YOLO model, with deployment support for Docker, Kubernetes, Terraform-provisioned Google Cloud infrastructure, and Locust load testing.

## Project Overview

The project demonstrates how a machine learning model can be packaged as a production-style API and deployed on container infrastructure. Users submit base64-encoded images to the API, and the service returns detected waste classes, bounding boxes, confidence scores, inference timing, or a base64-encoded annotated image.

The system was designed around a practical deployment workflow:

1. Package the FastAPI inference service in Docker.
2. Deploy the container to Kubernetes with CPU and memory limits.
3. Provision cloud virtual machines and firewall rules with Terraform.
4. Benchmark API throughput and latency with Locust.

## Key Features

- FastAPI inference service with `/api/predict` and `/api/annotate` endpoints.
- YOLO-based object detection using Ultralytics.
- Base64 image request and response handling.
- Docker multi-stage build for a lean runtime image.
- Kubernetes deployment with readiness/liveness probes and resource limits.
- Terraform configuration for Google Cloud VM infrastructure.
- Locust benchmark script for concurrent request testing.
- CPU-thread environment controls for predictable inference benchmarking.

## Tech Stack

- Python
- FastAPI
- Ultralytics YOLO
- PyTorch CPU runtime
- OpenCV
- Docker
- Kubernetes
- Terraform
- Google Cloud Platform
- Locust

## Repository Structure

```text
cloud-eco-waste-detection-api/
├── README.md
├── Dockerfile
├── requirements_api.txt
├── locustfile.py
├── resize_benchmark_image.py
├── main.py
├── inference.py
├── schemas.py
├── utils.py
├── runs/
│   └── detect/
│       └── train/
│           └── weights/
│               └── best.pt
├── test_images/
│   └── benchmark_sample.jpg
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
└── terraform/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── startup-common.sh
    └── terraform.tfvars.example
```

## API Endpoints

### Health Check

```http
GET /
```

Response:

```json
{
  "message": "CloudEco API is running"
}
```

### Predict Waste Objects

```http
POST /api/predict
```

Request body:

```json
{
  "uuid": "example-id",
  "image": "base64_encoded_image_string"
}
```

Response body:

```json
{
  "uuid": "example-id",
  "count": 2,
  "detections": ["Plastic Bottle", "Other Waste"],
  "boxes": [
    {
      "x": 120.45,
      "y": 80.12,
      "width": 210.5,
      "height": 350.25,
      "probability": 0.9234
    }
  ],
  "speed_preprocess_ms": 2.31,
  "speed_inference_ms": 412.76,
  "speed_postprocess_ms": 1.15
}
```

### Return Annotated Image

```http
POST /api/annotate
```

Response body:

```json
{
  "uuid": "example-id",
  "image": "base64_encoded_annotated_image"
}
```

## Model

The model file is expected at:

```text
runs/detect/train/weights/best.pt
```

Detected classes are mapped to portfolio-friendly labels:

| Raw Label | API Label |
|---|---|
| `PLASTIC_BAG` | Plastic Bag |
| `PLASTIC_BOTTLE` | Plastic Bottle |
| `OTHER_PLASTIC_WASTE` | Other Waste |
| `NOT_PLASTIC_WASTE` | Not Plastic Waste |

## Run Locally

Install dependencies:

```bash
pip install -r requirements_api.txt
```

Start the API:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Test the health endpoint:

```bash
curl http://localhost:8000/
```

## Docker

Build the image from the repository root:

```bash
docker build -t cloud-eco-api .
```

Run the container:

```bash
docker run -p 8000:8000 cloud-eco-api
```

## Kubernetes

Apply the Kubernetes manifests:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Check rollout status:

```bash
kubectl rollout status deployment/cloud-eco-api
kubectl get pods
kubectl get services
```

The service exposes the API through NodePort `30080`.

## Terraform

The Terraform configuration provisions Google Cloud virtual machines and firewall rules for a small Kubernetes cluster.

Create a local variable file from the safe example:

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
```

Update `terraform.tfvars` with your own GCP project details, then run:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Do not commit real `terraform.tfvars`, Terraform state files, service account JSON files, or private SSH keys.

## Load Testing

The Locust benchmark script sends requests to both prediction and annotation endpoints.

Run Locust from the repository root:

```bash
locust -f locustfile.py --host http://localhost:8000
```

Then open:

```text
http://localhost:8089
```

## Benchmark Summary

The deployment was benchmarked across different Kubernetes replica counts.

| Pods | Best Stable Users | Best Stable RPS | Average Latency | Failure Rate |
|---:|---:|---:|---:|---:|
| 1 | 6 | 1.6 | 1692.96 ms | 0% |
| 2 | 12 | 3.0 | 1850.30 ms | 0% |
| 4 | 20 | 5.1 | 1800.49 ms | 0% |
| 8 | 40 | 10.4 | 1784.17 ms | 0% |

The best stable result was 8 pods, 40 users, 10.4 RPS, and 0% request failures.

## Portfolio Summary

This project demonstrates cloud-native ML deployment skills across API design, model serving, containerisation, Kubernetes orchestration, infrastructure as code, and performance testing. It shows how a computer vision model can be moved from a trained artifact into a deployable, benchmarked service.




