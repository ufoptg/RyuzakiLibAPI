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
import json
import base64
import re
import uvicorn
import os
import shutil
import random
import g4f
import tempfile
import io
from io import BytesIO
from datetime import datetime as dt
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from typing import Union
from typing_extensions import Annotated
from typing import Annotated, Union

from pydantic import BaseModel
from base64 import b64decode as kc
from base64 import b64decode
from random import choice
from gpytranslate import SyncTranslator
from httpx import AsyncClient
from telegraph import Telegraph, upload_file
from pathlib import Path
from serpapi import GoogleSearch

from fastapi import FastAPI, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi import HTTPException
from fastapi import FastAPI, Request, Header
from fastapi import Body, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse

from templates.config import *
from RyuzakiLib.spamwatch.clients import SibylBan

logging.basicConfig(level=logging.ERROR)

app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    version=VERSION,
    terms_of_service=TERMS_OF_SERVICE,
    docs_url=DOCS_URL
)

@app.get("/test")
def hello_world():
    return {"message": "hello world"}

@app.get("/ryuzaki/blacklist-words")
def blacklist_words():
    try:
        BLACKLIST_WORDS = BadWordsList()
        results_all = BLACKLIST_WORDS.banned_by_google(file_txt="banned_by_google.txt", storage=True)
        return {"status": "true", "results": results_all}
    except Exception as e:
        return {"status": "false", "message": f"Internal server error: {str(e)}"}

@app.post("/ryuzaki/sibylban")
def sibyl_system_ban(
    user_id: int = Query(..., description="User ID in query parameter"),
    reason: str = Query(..., description="Reason in query parameter"),
    api_key: str = Query(..., description="Api key in query parameter")
):
    if user_id != TELEGRAM_ID:
        return {"status": "false", "message": "Only Developer"}

    clients = SiblyBan(api_key=api_key)
    try:
        response = clients.get_ban(user_id=user_id, banlist=True)
        sibyl_user_id = response.get("randydev", {}).get("sibyl_user_id")
        if sibyl_user_id:
            return {"status": "false", "message": "User is already banned"}

        response_str = clients.add_ban(user_id=user_id, reason=reason, is_banned=True)
        return {
            "status": "true",
            "results": {
                "message": response_str
            }
        }
    except Exception as e:
        logging.error(f"Error in sibyl_system_ban: {e}")
        return {"status": "false", "message": "Internal server error"}
