
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# live2d assets server
# http://127.0.0.1:8000/assets/*

# 依赖
# pip install fastapi
# pip install uvicorn

# uvicorn apiserver:app 

app = FastAPI()

app.mount("/assets", StaticFiles(directory="./assets"), name="static")

print("listening .......")