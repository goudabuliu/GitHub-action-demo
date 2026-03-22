from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello FastAPI from Aliyun FC3"}

# 适配FC
handler = app