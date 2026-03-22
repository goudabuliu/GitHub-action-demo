from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def hello():
    """返回HTML页面，在网页上显示helloworld"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI on FC3</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            .container {
                text-align: center;
                background: white;
                padding: 3rem;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            }
            h1 {
                color: #333;
                font-size: 3rem;
                margin-bottom: 1rem;
            }
            p {
                color: #666;
                font-size: 1.2rem;
            }
            .highlight {
                color: #667eea;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello World! 🌍</h1>
            <p>这是一个运行在 <span class="highlight">阿里云函数计算 FC3</span> 上的 FastAPI 应用</p>
            <p>当前时间: <span id="current-time">loading...</span></p>
            <p>部署状态: <span class="highlight">✅ 运行正常</span></p>
        </div>
        <script>
            // 显示当前时间
            function updateTime() {
                const now = new Date();
                const timeString = now.toLocaleString('zh-CN', {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: false
                });
                document.getElementById('current-time').textContent = timeString;
            }
            updateTime();
            setInterval(updateTime, 1000);
        </script>
    </body>
    </html>
    """
    return html_content

def handler(event, context):
    """
    FC3 HTTP事件处理器 - 优化版本
    处理HTTP触发器事件并返回HTML响应
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

        # 如果是根路径，返回HTML页面
        if path == "/" and http_method == "GET":
            html_content = hello()  # 获取HTML内容
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "text/html; charset=utf-8",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": html_content
            }
        else:
            # 404错误页面 - 返回简单HTML
            error_html = """
            <!DOCTYPE html>
            <html>
            <head><title>404 Not Found</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1>404 - 页面未找到</h1>
                <p>请求的路径 <strong>{}</strong> 不存在</p>
                <p><a href="/">返回首页</a></p>
            </body>
            </html>
            """.format(path)
            return {
                "statusCode": 404,
                "headers": {"Content-Type": "text/html; charset=utf-8"},
                "body": error_html
            }

    except Exception as e:
        # 500错误页面 - 返回简单HTML
        error_html = """
        <!DOCTYPE html>
        <html>
        <head><title>500 Server Error</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h1>500 - 服务器错误</h1>
            <p>错误信息: <strong>{}</strong></p>
            <p><a href="/">返回首页</a></p>
        </body>
        </html>
        """.format(str(e).replace('<', '&lt;').replace('>', '&gt;'))
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "text/html; charset=utf-8"},
            "body": error_html
        }