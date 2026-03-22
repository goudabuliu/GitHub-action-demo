from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello FastAPI from Aliyun FC3"}

def handler(event, context):
    """
    FC3 HTTP事件处理器 - 简化版本
    处理HTTP触发器事件并返回响应
    """
    try:
        # 解析FC3 HTTP事件
        # FC3 HTTP事件格式通常包含：
        # - httpMethod: HTTP方法
        # - path: 请求路径
        # - headers: 请求头
        # - queryParameters: 查询参数
        # - body: 请求体
        http_method = event.get("httpMethod", "GET")
        path = event.get("path", "/")

        # 如果是根路径，返回FastAPI响应
        if path == "/" and http_method == "GET":
            response_data = hello()
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": json.dumps(response_data, ensure_ascii=False)
            }
        else:
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Not Found"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)})
        }