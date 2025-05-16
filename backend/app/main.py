from fastapi import FastAPI
from app.database import init_db

app = FastAPI()

init_db()  # 여기서 models.py 내부 import 및 테이블 생성

@app.get("/")
def root():
    return {"message": "EasyBank API is running"}

