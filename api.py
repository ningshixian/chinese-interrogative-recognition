import time
import sys
import numpy as np
import asyncio
import uvicorn
import json
from fastapi import FastAPI
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator
from starlette.testclient import TestClient

from schemas.response import response_code
from logger import logger, log_filter
import interrogative_classifier as ic


"""
nohup python api.py  > logs/api.log.txt 2>&1 &
gunicorn api:app -b 0.0.0.0:8085 -w 1 --threads 20 -k uvicorn.workers.UvicornWorker
pkill -f "gunicorn api:app -b 0.0.0.0:8085"
"""

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Item(BaseModel):
    """请求体参数"""
    text: str


@app.post("/interrogative")
@log_filter
def seat_rec(request: Request, item: Item):
    json_data = item.dict()
    query = json_data["text"]

    # 异常情况处理
    if not query:
        return response_code.resp_4001(message="输入不可为空！")

    result_list = ic.func(query, ic.special_token)
    return response_code.resp_200(result_list=result_list)


if __name__ == "__main__":

    uvicorn.run(
        app="api:app",
        host="0.0.0.0",
        port=8085,
        backlog=2048,
        limit_concurrency=200,
        workers=1,
        reload=True,
        # debug=True,
    )
