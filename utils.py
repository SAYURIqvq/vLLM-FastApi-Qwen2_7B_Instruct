import time
from datetime import datetime
from pydantic import BaseModel


def get_current_time():
    '''
    功能：获取当前时间，时间格式：yyyy-mm-dd hh:mm:ss
    '''
    # 获取当前时间
    current_time = datetime.now()
    # 格式化为 "yyyy-mm-dd hh:mm:ss:fff" 格式
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return formatted_time


def make_serializable(obj):
    if isinstance(obj, BaseModel):
        return obj.dict()
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    else:
        return obj

