from fastapi import FastAPI, HTTPException
from starlette.concurrency import run_in_threadpool

from schemas import PredictRequest
from utils import decode_base64_image
from inference import run_prediction, render_annotated_base64

app = FastAPI()


@app.get("/")
def root():
    return {"message": "CloudEco API is running"}


@app.post("/api/predict")
async def predict(request: PredictRequest):
    try:
        image = await run_in_threadpool(decode_base64_image, request.image)

        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image data")

        prediction = await run_in_threadpool(run_prediction, image)

        return {
            "uuid": request.uuid,
            "count": prediction["count"],
            "detections": prediction["detections"],
            "boxes": prediction["boxes"],
            "speed_preprocess_ms": prediction["speed_preprocess_ms"],
            "speed_inference_ms": prediction["speed_inference_ms"],
            "speed_postprocess_ms": prediction["speed_postprocess_ms"],
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/annotate")
async def annotate(request: PredictRequest):
    try:
        image = await run_in_threadpool(decode_base64_image, request.image)

        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image data")

        prediction = await run_in_threadpool(run_prediction, image)
        annotated_base64 = await run_in_threadpool(render_annotated_base64, prediction)

        return {
            "uuid": request.uuid,
            "image": annotated_base64,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
