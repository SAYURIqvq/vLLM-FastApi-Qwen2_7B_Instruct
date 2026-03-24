from pydantic import BaseModel
from typing import List,Dict,Literal


class Message(BaseModel):
    role:Literal["user", "assistant", "system"]
    content:str
    class Config:
        extra = "ignore"

class APIRequest(BaseModel):
    request_id: str
    request_time: str
    message: List[Message]
    class Config:
        extra = "ignore"


class VLLMRequest(BaseModel):
    request_id: str
    request_time: str
    prompt: str

    class Config:
        extra = "ignore"

