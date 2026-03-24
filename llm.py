import uuid
# from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams
from vllm import SamplingParams
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import AsyncLLMEngine
import asyncio
from typing import AsyncGenerator
import json
from utils import get_current_time
from dataStruct import VLLMRequest

class VLLM:
    def __init__(self, MODEL_ID: str) -> None:
        self.MODEL_ID = MODEL_ID
        self.MAX_TOKENS = 1024
        ENGINE_ARGS = AsyncEngineArgs(
            model=self.MODEL_ID,
            max_model_len=self.MAX_TOKENS,
            tensor_parallel_size=1,
            gpu_memory_utilization=0.90,
            enforce_eager=False,  # capture the graph for faster inference, but slower cold starts
            disable_log_stats=True,  # disable logging so we can stream tokens
            disable_log_requests=True,
        )
        self.engine = AsyncLLMEngine.from_engine_args(ENGINE_ARGS)

    def build_prompt(self,user_prompt:str) -> str:
        PROMPT_TEMPLATE = """你是一个人工智能助手，擅长根据用户提供的资料来回答用户的问题。
                请务必严格按照用户提供的参考资料来回答用户的问题，不要编造资料中不存在的内容。
                如果用户提供的资料不能让你十分有信心地回答用户的问题，则明确告诉用户欠缺必要的参考资料，无法直接回答当前问题。
                {user_prompt}"""
        prompt = PROMPT_TEMPLATE.format(user_prompt=user_prompt)
        return prompt

    async def generate(self, data:VLLMRequest) -> AsyncGenerator[str, None]:
        SAMPLING_PARAM = SamplingParams(
            max_tokens=self.MAX_TOKENS,
            frequency_penalty=1.0,
            temperature=0.1,
            seed=42,
            skip_special_tokens=True,
            length_penalty=1.0,

        )
        prompt = self.build_prompt(user_prompt=data.prompt)
        llm_output = await self.engine.add_request(uuid.uuid4().hex, prompt, SAMPLING_PARAM)
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



