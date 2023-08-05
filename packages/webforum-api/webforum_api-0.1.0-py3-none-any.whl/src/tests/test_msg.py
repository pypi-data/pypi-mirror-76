#!/usr/bin/python3
# coding: utf-8
# author: Clement Onawole - dapo.onawole@gmail.com
# test_msg.py

import json, pytest

from fastapi import Body, FastAPI, Request, Response
from fastapi.testclient import TestClient

from ..app import msApp

client = TestClient(msApp)

def test_get_build():
    response = client.get('/api/msg/v1')

    assert response.status_code == 200
    assert response.json() == { 'service': f'{msApp.title} v{msApp.version}' }