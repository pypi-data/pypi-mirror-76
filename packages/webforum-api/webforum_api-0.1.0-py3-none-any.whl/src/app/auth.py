#!usr/bin/python3
# coding: utf-8
# author: Clement Onawole - dapo.onawole@gmail.com
# auth.api.py

import uvicorn, gzip, json, time, logging, random, string

from fastapi import Body, FastAPI, Request, Response
from fastapi.routing import APIRoute

app = FastAPI(
    title='Auth Services',
    version='0.1.0'
)

@app.get('/api/auth/v1')
async def read_root():
    return {"service": f"{app.title} v{app.version}" }


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001, debug='true')