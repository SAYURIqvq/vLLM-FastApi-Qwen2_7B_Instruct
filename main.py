from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import uvicorn
import json

from config import get_settings
from llm import VLLM
from dataStruct import VLLMRequest,APIRequest
from utils import get_current_time

settings = get_settings()
app = FastAPI()
llm = None


def get_llm() -> VLLM:
    """Lazily initialize the vLLM engine on first generation request."""
    global llm
    if llm is None:
        llm = VLLM(settings)
    return llm


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model_id": settings.model_id,
        "engine_loaded": llm is not None,
    }

@app.post("/generate/")
async def generate_text(data: APIRequest):
    if not data.message:
        raise HTTPException(status_code=400, detail="message must not be empty")
    if data.message[-1].role == "user":
        vllmRequest = VLLMRequest(**{
                                        "request_id": data.request_id,
                                        "request_time": data.request_time,
                                        "prompt": data.message[-1].content
                                    })
    else:
        raise HTTPException(status_code=400, detail="last message role must be user")
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }

    async def generator():
        async for chunk in get_llm().generate(data=vllmRequest):
            chunk["fastAPI_accept_chunk_time"] = get_current_time()
            print(f"fastapi chunk: {chunk}")
            yield f"{json.dumps(chunk, ensure_ascii=False)}\n"

    return StreamingResponse(generator(),
                             # media_type="application/json",
                             media_type="text/event-stream",
                             headers=headers)


if __name__ == '__main__':
    uvicorn.run(app, host=settings.host, port=settings.port)
