from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.predictor import Predictor
from app.schemas import PredictionResponse, StudentFeatures

predictor: Predictor | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global predictor
    predictor = Predictor()
    yield


app = FastAPI(
    title="Student Performance Prediction API",
    description="Predicts whether a student will pass or fail based on academic and behavioral features.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {"message": "Student Performance Prediction API is running. See /docs for usage."}


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": predictor is not None}


@app.post("/predict", response_model=PredictionResponse)
def predict(features: StudentFeatures):
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model is not loaded yet")
    result = predictor.predict(features.model_dump())
    return result
