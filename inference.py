from ultralytics import YOLO
import os

MODEL_PATH = "runs/detect/train/weights/best.pt"

LABEL_MAP = {
    "PLASTIC_BAG": "Plastic Bag",
    "PLASTIC_BOTTLE": "Plastic Bottle",
    "OTHER_PLASTIC_WASTE": "Other Waste",
    "NOT_PLASTIC_WASTE": "Not Plastic Waste"
}

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

model = YOLO(MODEL_PATH)


def run_prediction(image):
    results = model.predict(
        source=image,
        save=False,
        verbose=False,
        imgsz=416
    )
    r = results[0]

    detections = []
    boxes = []

    if r.boxes is not None:
        for box in r.boxes:
            cls_id = int(box.cls[0].item())
            raw_name = model.names[cls_id]
            conf = float(box.conf[0].item())
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append(LABEL_MAP.get(raw_name, raw_name))
            boxes.append({
                "x": round(x1, 2),
                "y": round(y1, 2),
                "width": round(x2 - x1, 2),
                "height": round(y2 - y1, 2),
                "probability": round(conf, 4)
            })

    return {
        "count": len(detections),
        "detections": detections,
        "boxes": boxes,
        "speed_preprocess_ms": round(r.speed["preprocess"], 4),
        "speed_inference_ms": round(r.speed["inference"], 4),
        "speed_postprocess_ms": round(r.speed["postprocess"], 4),
        "result_object": r
    }


def render_annotated_base64(prediction):
    annotated = prediction["result_object"].plot()
    import cv2
    import base64

    success, buffer = cv2.imencode(".jpg", annotated)
    if not success:
        raise ValueError("Failed to encode image")

    return base64.b64encode(buffer).decode("utf-8")
