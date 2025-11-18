# src/train.py
"""
NimbusOps training entrypoint.

This script:
- loads a simple tabular dataset
- trains a classifier
- logs metrics and artifacts to MLflow
- writes a versioned model file under models/

You can swap the dataset / model without changing the contract with
downstream pipeline and prediction code.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"


@dataclass
class TrainConfig:
    test_size: float = 0.2
    random_state: int = 42
    max_iter: int = 1000
    C: float = 1.0


def load_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    For demo purposes we use sklearn's breast cancer dataset.
    In a real deployment, this would be a feature store / data warehouse read.
    """
    ds = load_breast_cancer(as_frame=True)
    X = ds.data.values
    y = ds.target.values
    return X, y


def create_model(cfg: TrainConfig) -> LogisticRegression:
    return LogisticRegression(
      max_iter=cfg.max_iter,
      C=cfg.C,
      solver="lbfgs",
    )


def train(cfg: TrainConfig) -> Path:
    X, y = load_data()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=cfg.test_size,
        random_state=cfg.random_state,
        stratify=y,
    )

    model = create_model(cfg)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    try:
        auc = roc_auc_score(y_test, y_proba)
    except Exception:
        auc = float("nan")

    print(f"[NimbusOps] accuracy={acc:.4f}  auc={auc:.4f}")

    # ---- MLflow logging ----------------------------------------------------
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", str(PROJECT_ROOT / "mlruns"))
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("nimbusops-breast-cancer")

    with mlflow.start_run(run_name="logreg-baseline") as run:
        mlflow.log_param("test_size", cfg.test_size)
        mlflow.log_param("max_iter", cfg.max_iter)
        mlflow.log_param("C", cfg.C)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("auc", auc)

        mlflow.sklearn.log_model(model, artifact_path="model")

        run_id = run.info.run_id
        print(f"[NimbusOps] Logged model to MLflow run: {run_id}")

    # ---- Local artifact save ----------------------------------------------
    MODELS_DIR.mkdir(exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    model_path = MODELS_DIR / f"model_logreg_{ts}.joblib"
    joblib.dump(model, model_path)
    print(f"[NimbusOps] Saved local model artifact: {model_path}")

    return model_path


def main() -> None:
    cfg = TrainConfig()
    train(cfg)


if __name__ == "__main__":
    main()
