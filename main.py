from fastapi import FastAPI
# from starlette.responses import StreamingResponse
from fastapi.responses import StreamingResponse
# from fastapi.responses import StreamingResponse,JSONResponse
import uvicorn
import json
from llm import VLLM
from dataStruct import VLLMRequest,APIRequest
from utils import get_current_time

llm = VLLM(MODEL_ID="/media/cara/文档/PythonProjects/models/llm/qwen/Qwen2-7B-Instruct")
app = FastAPI()

@app.post("/generate/")
async def generate_text(data: APIRequest):
    if data.message[-1].role == "user":
        vllmRequest = VLLMRequest(**{
                                        "request_id": data.request_id,
                                        "request_time": data.request_time,
                                        "prompt": data.message[-1].content
                                    })
    else:
        raise RuntimeError(f"API request data.message[-1].role is not a user")
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }

    async def generator():
        async for chunk in llm.generate(data=vllmRequest):
            chunk["fastAPI_accept_chunk_time"] = get_current_time()
            print(f"fastapi chunk: {chunk}")
            yield f"{json.dumps(chunk, ensure_ascii=False)}\n"

    return StreamingResponse(generator(),
                             # media_type="application/json",
                             media_type="text/event-stream",
                             headers=headers)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
