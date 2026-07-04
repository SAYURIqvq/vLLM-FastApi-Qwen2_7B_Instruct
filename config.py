"""Runtime configuration for the vLLM FastAPI service."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model_id: str
    max_tokens: int
    tensor_parallel_size: int
    gpu_memory_utilization: float
    temperature: float
    host: str
    port: int


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return default if value is None else int(value)


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return default if value is None else float(value)


def get_settings() -> Settings:
    """Load settings from environment variables."""
    return Settings(
        model_id=os.getenv("MODEL_ID", "Qwen/Qwen2-7B-Instruct"),
        max_tokens=_get_int("MAX_TOKENS", 1024),
        tensor_parallel_size=_get_int("TENSOR_PARALLEL_SIZE", 1),
        gpu_memory_utilization=_get_float("GPU_MEMORY_UTILIZATION", 0.90),
        temperature=_get_float("TEMPERATURE", 0.1),
        host=os.getenv("HOST", "0.0.0.0"),
        port=_get_int("PORT", 8080),
    )
