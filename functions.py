#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2020-2023 (c) Randy W @xtdevs, @xtsea
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
import database as db
from fastapi import HTTPException
from main import SOURCE_ALPHA_URL, ONLY_DEVELOPER_API_KEYS, HUGGING_TOKEN

def ryuzaki_ai_text(text):
    API_URL = SOURCE_ALPHA_URL
    headers = {"Authorization": f"Bearer {HUGGING_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    return response.json()

def validate_api_key(api_key: str = Header(...)):
    USERS_API_KEYS = db.get_all_api_keys()
    if api_key not in USERS_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

def validate_api_key_only_devs(api_key: str = Header(...)):
    if api_key not in ONLY_DEVELOPER_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
