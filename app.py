# app.py（FC3 + FastAPI 最简 HelloWorld）
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# 初始化 FastAPI 应用
app = FastAPI()

# 定义 HelloWorld 接口
@app.get("/")
async def root():
    return {
        "message": "Hello FastAPI on FC3! 🚀",
        "region": "cn-shenzhen",
        "framework": "FastAPI",
        "runtime": "python3.10"
    }

# FC3 函数入口（必须！FC 会调用这个 handler 函数）
def handler(event, context):
    # 解析 FC 事件（转换为 FastAPI 可处理的格式）
    try:
        # 模拟 FastAPI 请求处理
        path = event.get("path", "/")
        if path == "/":
            result = root()
            return JSONResponse(
                content=result,
                status_code=200,
                headers={"Access-Control-Allow-Origin": "*"}
            )
        else:
            return JSONResponse(
                content={"error": "Not Found"},
                status_code=404
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )