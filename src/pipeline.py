# src/pipeline.py
"""
High-level pipeline entrypoint for NimbusOps.

Right now this is intentionally simple:
- run a training job
- print out the model artifact path

In a real setup you would:
- push the artifact to S3
- update model registry
- trigger a deployment pipeline
"""

from __future__ import annotations

from pathlib import Path

from .train import TrainConfig, train


def main() -> None:
    cfg = TrainConfig()
    model_path: Path = train(cfg)
    print(f"[NimbusOps] Pipeline complete. Trained model at: {model_path}")


if __name__ == "__main__":
    main()
