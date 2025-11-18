# src/predict.py
"""
NimbusOps prediction service.

Exposes a small FastAPI app that:
- loads the most recent model from models/
- exposes POST /predict for inference

This is deliberately lightweight but structured like something
you would containerize and deploy behind a load balancer.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conlist


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"

app = FastAPI(title="NimbusOps Prediction API", version="0.1.0")

_model = None  # lazy-loaded


class PredictionRequest(BaseModel):
    features: List[conlist(float, min_items=1)]


class PredictionResponse(BaseModel):
    predictions: List[int]
    probabilities: List[float]


def _get_latest_model_path() -> Path:
    if not MODELS_DIR.exists():
        raise RuntimeError(f"Models directory not found: {MODELS_DIR}")

    candidates = sorted(MODELS_DIR.glob("model_logreg_*.joblib"))
    if not candidates:
        raise RuntimeError(f"No model artifacts found in {MODELS_DIR}")
    return candidates[-1]


def load_model():
    global _model
    if _model is None:
        path = _get_latest_model_path()
        _model = joblib.load(path)
        print(f"[NimbusOps] Loaded model from {path}")
    return _model


@app.on_event("startup")
def on_startup() -> None:
    load_model()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest) -> PredictionResponse:
    model = load_model()

    if not req.features:
        raise HTTPException(status_code=400, detail="No feature rows provided.")

    X = np.array(req.features, dtype=float)
    try:
        y_pred = model.predict(X)
        y_proba = model.predict_proba(X)[:, 1]
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Model inference failed: {exc}")

    return PredictionResponse(
        predictions=[int(x) for x in y_pred],
        probabilities=[float(p) for p in y_proba],
    )
