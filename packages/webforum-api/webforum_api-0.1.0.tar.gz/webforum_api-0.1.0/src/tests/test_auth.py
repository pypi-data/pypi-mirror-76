#!/usr/bin/python3
# coding: utf-8
# author: Clement Onawole - dapo.onawole@gmail.com
# test_auth.py

import json, pytest
from ..app import auApp

from fastapi import Body, FastAPI, Request, Response
from fastapi.testclient import TestClient

client = TestClient(auApp)

def test_get_build():
    response = client.get('/api/auth/v1')

    assert response.status_code == 200
    assert response.json() == { 'service': f'{auApp.title} v{auApp.version}' }