# vLLM-FastAPI-Qwen2_7B_Instruct

本项目基于 FastAPI 构建，结合 vLLM 实现对 **Qwen2-7B-Instruct** 模型的高性能推理服务，适用于对大语言模型进行部署与服务化的场景。

---

## 项目简介

该服务提供标准的 RESTful 接口，用于处理对话式请求。通过 vLLM 提供高吞吐、低延迟的推理能力，并使用 Pydantic 对请求数据进行结构化校验，保证接口的稳定性与可维护性。

---

## 项目结构

```
.
├── main.py          # FastAPI 应用入口
├── llm.py           # vLLM 模型加载与推理逻辑
├── dataStruct.py    # 请求数据结构定义（Pydantic 模型）
├── utils.py         # 工具函数
├── api_test.py      # 接口测试脚本
├── requirements.txt # 依赖列表
└── README.md        # 项目说明文档
```

---

## 数据结构说明

项目中定义了统一的请求数据格式，位于 `dataStruct.py`：

### Message

用于表示单轮对话内容：

* `role`：消息角色，可选值为 `"user"`、`"assistant"`、`"system"`
* `content`：消息文本内容

### APIRequest

用于接收外部 API 请求：

* `request_id`：请求唯一标识
* `request_time`：请求时间
* `message`：消息列表（多轮对话）

### VLLMRequest

用于传递给 vLLM 的请求结构：

* `request_id`：请求唯一标识
* `request_time`：请求时间
* `prompt`：拼接后的模型输入文本

---

## 安装依赖

建议使用 Python 3.10 及以上版本。

```bash
pip install -r requirements.txt
```

---

## 启动服务

```bash
python main.py
```

或使用 uvicorn：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 接口说明

### 请求示例

```json
{
  "request_id": "123456",
  "request_time": "2026-03-24 12:00:00",
  "message": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "你好"
    }
  ]
}
```

### 返回说明

返回内容通常为模型生成的文本结果，具体格式取决于 `main.py` 中的实现逻辑。

---

## 说明

* 本项目仅提供基础推理服务框架，可根据实际需求扩展鉴权、日志、限流等功能。
* 推荐在 GPU 环境下运行，以获得更优的性能表现。
* vLLM 相关配置（如并发、显存管理等）可在 `llm.py` 中调整。

---

## License

This project is provided for research and development purposes. Please comply with the license terms of Qwen and vLLM when using this project.
