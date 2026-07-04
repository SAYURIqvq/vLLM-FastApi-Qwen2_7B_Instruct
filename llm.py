import uuid
import asyncio
from typing import AsyncGenerator

from config import Settings
from utils import get_current_time
from dataStruct import VLLMRequest

class VLLM:
    def __init__(self, settings: Settings) -> None:
        from vllm import SamplingParams
        from vllm.engine.arg_utils import AsyncEngineArgs
        from vllm.engine.async_llm_engine import AsyncLLMEngine

        self.settings = settings
        self.SamplingParams = SamplingParams
        engine_args = AsyncEngineArgs(
            model=settings.model_id,
            max_model_len=settings.max_tokens,
            tensor_parallel_size=settings.tensor_parallel_size,
            gpu_memory_utilization=settings.gpu_memory_utilization,
            enforce_eager=False,  # capture the graph for faster inference, but slower cold starts
            disable_log_stats=True,  # disable logging so we can stream tokens
            disable_log_requests=True,
        )
        self.engine = AsyncLLMEngine.from_engine_args(engine_args)

    def build_prompt(self,user_prompt:str) -> str:
        PROMPT_TEMPLATE = """你是一个人工智能助手，擅长根据用户提供的资料来回答用户的问题。
                请务必严格按照用户提供的参考资料来回答用户的问题，不要编造资料中不存在的内容。
                如果用户提供的资料不能让你十分有信心地回答用户的问题，则明确告诉用户欠缺必要的参考资料，无法直接回答当前问题。
                {user_prompt}"""
        prompt = PROMPT_TEMPLATE.format(user_prompt=user_prompt)
        return prompt

    async def generate(self, data:VLLMRequest) -> AsyncGenerator[str, None]:
        sampling_param = self.SamplingParams(
            max_tokens=self.settings.max_tokens,
            frequency_penalty=1.0,
            temperature=self.settings.temperature,
            seed=42,
            skip_special_tokens=True,
            length_penalty=1.0,

        )
        prompt = self.build_prompt(user_prompt=data.prompt)
        llm_output = await self.engine.add_request(uuid.uuid4().hex, prompt, sampling_param)
        cursor = 0
        async for request_output in llm_output:
            text = request_output.outputs[0].text

            current_text = text[cursor:]
            output = {
                "text": current_text,
                "llm_response_time": get_current_time(),
                "request_id":data.request_id,
                "request_time":data.request_time,
                "stream_uuid": str(uuid.uuid4()),
                # "prompt": prompt,
            }
            # print(f"vLLM chunk:{output}")
            yield output
            cursor = len(text)
            await asyncio.sleep(0.01)


