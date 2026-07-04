import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import get_settings
from llm import VLLM


def test_settings_load_from_environment(monkeypatch):
    monkeypatch.setenv("MODEL_ID", "Qwen/Qwen2-7B-Instruct")
    monkeypatch.setenv("MAX_TOKENS", "512")
    monkeypatch.setenv("TENSOR_PARALLEL_SIZE", "2")
    monkeypatch.setenv("GPU_MEMORY_UTILIZATION", "0.75")

    settings = get_settings()

    assert settings.model_id == "Qwen/Qwen2-7B-Instruct"
    assert settings.max_tokens == 512
    assert settings.tensor_parallel_size == 2
    assert settings.gpu_memory_utilization == 0.75


def test_prompt_template_requires_grounding():
    prompt = VLLM.build_prompt(None, "参考资料：A。问题：B？")

    assert "严格按照用户提供的参考资料" in prompt
    assert "不要编造" in prompt
    assert "参考资料：A" in prompt
