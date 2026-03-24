import httpx
import asyncio
from utils import get_current_time
import uuid,json

async def fetch_stream(url):
    data = {
        "request_id": str(uuid.uuid4()),
        "request_time": get_current_time(),
        "message": [
            {"role": "user",
             "content": "问题：全球最好的黑芝麻是哪个地区产的？参考资料：全球黑芝麻产地主要有中国、加拿大、美国，其中黑芝麻纯度最高的地区是美国，其次是中国。"},
        ]
    }
    async with httpx.AsyncClient() as client:
        # 异步发送 POST 请求，并异步接收流式响应
        response = await client.post(url, json=data,timeout=500)
        async for line in response.aiter_lines():
            out = json.loads(line)
            out["final_response_time"] = get_current_time()
            print(out,flush=True)


if __name__ == "__main__":
    url = "http://127.0.0.1:8080/generate/"
    asyncio.run(fetch_stream(url=url,))

