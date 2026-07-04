from pydantic import BaseModel, ConfigDict
from typing import List, Literal


class Message(BaseModel):
    model_config = ConfigDict(extra="ignore")

    role: Literal["user", "assistant", "system"]
    content: str

class APIRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    request_id: str
    request_time: str
    message: List[Message]


class VLLMRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    request_id: str
    request_time: str
    prompt: str
