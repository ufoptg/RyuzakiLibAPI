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

from RyuzakiLib.hackertools.chatgpt import RendyDevChat
from RyuzakiLib.hackertools.openai import OpenAiToken
from RyuzakiLib.mental import BadWordsList

import logging
import database as db
import functions as code

logging.basicConfig(level=logging.ERROR)

# I DON'T KNOW LIKE THIS HACKER
load_dotenv()
REVERSE_IMAGE_API = os.environ["REVERSE_IMAGE_API"]
OCR_API_KEY = os.environ["OCR_API_KEY"]
ONLY_DEVELOPER_API_KEYS = os.environ["ONLY_DEVELOPER_API_KEYS"]
HUGGING_TOKEN = os.environ["HUGGING_TOKEN"]
SOURCE_UNSPLASH_URL = os.environ["SOURCE_UNSPLASH_URL"]
SOURCE_OCR_URL = os.environ["SOURCE_OCR_URL"]
SOURCE_ALPHA_URL = os.environ["SOURCE_ALPHA_URL"]
SOURCR_WAIFU_URL = os.environ["SOURCE_ALPHA_URL"]
SOURCR_TIKTOK_WTF_URL = os.environ["SOURCR_TIKTOK_WTF_URL"]
SOURCR_TIKTOK_TECH_URL = os.environ["SOURCR_TIKTOK_TECH_URL"]
DEVELOPER_ID = os.environ["DEVELOPER_ID"]

description = """ 
- Ryuzaki Library: [Library Here](https://github.com/TeamKillerX/RyuzakiLib)

•Developed by [@xtdevs](https://t.me/xtdevs)
"""

app = FastAPI(
    title="RyuzakiLib API",
    description=description,
    version="1.3.1",
    terms_of_service="Use It Only For Personal Project Else I Need To Delete The Api",
    contact={
        "name": "RyuzakiLib",
        "url": "https://t.me/xtdevs",
        "email": "killerx@randydev.my.id",
    },
    docs_url="/"
)

def validate_api_key(api_key: str = Header(...)):
    USERS_API_KEYS = db.get_all_api_keys()
    if api_key not in USERS_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

def validate_api_key_only_devs(api_key: str = Header(...)):
    if api_key not in ONLY_DEVELOPER_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/ryuzaki/getbanlist")
def sibyl_get_all_banlist():
    banned_users = db.get_all_banned()
    return {
        "status": "True",
        "randydev": {
            "results": banned_users
        }
    }

@app.get("/ryuzaki/blacklist-words")
def blacklist_words():
    try:
        BLACKLIST_WORDS = BadWordsList()
        results_all = BLACKLIST_WORDS.banned_by_google(file_txt="banned_by_google.txt", storage=True)
        return {"status": "true", "results": results_all}
    except Exception as e:
        return {"status": "false", "message": f"Internal server error: {str(e)}"}

@app.delete("/ryuzaki/sibyldel")
def sibyl_system_delete(
    user_id: int = Query(..., description="User ID in query parameter only developer"),
    api_key: None = Depends(validate_api_key_only_devs)
):
    try:
        _, _, _, _, sibyl_user_id = db.get_sibyl_system_banned(user_id)

        if sibyl_user_id:
            db.remove_sibyl_system_banned(user_id)
            return {"status": "true", "message": f"Successfully removed {user_id} from the Sibyl ban list."}
        else:
            return {"status": "false", "message": "Not found user"}
    except Exception as e:
        return {"status": "false", "message": f"Internal server error: {str(e)}"}

@app.post("/ryuzaki/sibylban")
def sibyl_system_ban(
    user_id: int = Query(..., description="User ID in query parameter"),
    reason: str = Query(..., description="Reason in query parameter"),
    api_key: None = Depends(validate_api_key)
):
    if user_id != DEVELOPER_ID:
        return {"status": "false", "message": "Only Developer"}

    try:
        date_joined = str(dt.now())
        sibyl_ban = random.choice(db.RAMDOM_STATUS)
        _, _, is_banned, _, sibyl_user_id = get_sibyl_system_banned(user_id)

        if sibyl_user_id and is_banned:
            return {"status": "false", "message": "User is already banned"}

        db.new_sibyl_system_banned(user_id, sibyl_ban, reason, date_joined)

        return {
            "status": "true",
            "randydev": {
                "user_id": user_id,
                "sibyl_name": sibyl_ban,
                "reason": reason,
                "date_joined": date_joined,
                "message": f"Successfully banned {user_id} from the Sibyl ban list."
            }
        }
    except Exception as e:
        logging.error(f"Error in sibyl_system_ban: {e}")
        return {"status": "false", "message": "Internal server error"}

@app.get("/ryuzaki/sibyl")
def sibyl_system(
    user_id: int = Query(..., description="User ID in query parameter"),
    api_key: None = Depends(validate_api_key)
):
    sibyl_name, reason, is_banned, date_joined, sibyl_user_id = db.get_sibyl_system_banned(user_id)
    if sibyl_name and reason and is_banned and date_joined and sibyl_user_id:
        return {
            "status": "true",
            "randydev": {
                "sibyl_name": sibyl_name,
                "reason": reason,
                "is_banned": is_banned,
                "date_joined": date_joined,
                "sibyl_user_id": sibyl_user_id
            }
        }
    else:
        return {"status": "false", "message": "Not Found User"}

@app.get("/ryuzaki/ai")
def ryuzaki_ai(
    text: str = Query(..., description="text in query parameter"),
    api_key: None = Depends(validate_api_key)
):
    try:
        response_data = code.ryuzaki_ai_text(text)
        
        if isinstance(response_data, list) and len(response_data) > 0:
            first_result = response_data[0]
            if "generated_text" in first_result:
                message = first_result["generated_text"]
                return {
                    "status": "true",
                    "randydev": {
                        "ryuzaki_text": message
                    }
                }
        
        return {"status": "false", "message": "Invalid response format"}
        
    except Exception as e:
        return {"status": "false", "message": f"error: {e}"}

@app.get("/ryuzaki/unsplash")
async def get_image_unsplash(query: str, size: str="500x500"):
    url = SOURCE_UNSPLASH_URL
    image_url = f"{url}/?{query}/{size}"

    try:
        response = requests.get(image_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching image: {e}")

    return StreamingResponse(BytesIO(response.content), media_type="image/jpeg")

@app.get("/ryuzaki/reverse")
def google_reverse(
    engine: str="google_reverse_image",
    image_url: str=None,
    language: str="en",
    google_lang: str="us",
    api_key: None = Depends(validate_api_key)
):
    params = {
        "api_key": REVERSE_IMAGE_API,
        "engine": engine,
        "image_url": image_url,
        "hl": language,
        "gl": google_lang
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        link = results["search_metadata"]["google_reverse_image_url"]
        total_time_taken = results["search_metadata"]["total_time_taken"]
        create_at = results["search_metadata"]["created_at"]
        processed_at = results["search_metadata"]["processed_at"]
        return {
            "status": "true",
            "randydev": {
                "link": link,
                "total_time_taken": total_time_taken,
                "create_at": create_at,
                "processed_at": processed_at
            }
        }
    except Exception as e:
        return {"status": "false", "message": f"Error {e}"}

@app.get("/ryuzaki/ocr")
def ocr_space_url(
    url: str = Query(..., description="URL in query parameter"),
    overlay: bool=False,
    language: str = Query("eng", description="Language in query parameter"),
    api_key: None = Depends(validate_api_key)
):
    payload = {
        "url": url,
        "isOverlayRequired": overlay,
        "apikey": OCR_API_KEY,
        "language": language
    }
    try:
        response = requests.post(SOURCE_OCR_URL, data=payload)
        response.raise_for_status()
        test_url = response.content.decode()
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
    try:
        parsed_response = json.loads(test_url)
        if "ParsedResults" in parsed_response and len(parsed_response["ParsedResults"]) > 0:
            return {
                "status": "true",
                "randydev":{
                    "text": parsed_response["ParsedResults"][0]["ParsedText"]
                }
            }
        else:
            return {"status": "false", "message": "Error response."}
    except (json.JSONDecodeError, KeyError):
        return "Error parsing the OCR response."

@app.get("/ryuzaki/chatgpt4")
def chatgpt4_support(
    query: str=None,
    api_key: None = Depends(validate_api_key)
):
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": query}],
        )
        return {
            "status": "true",
            "randydev":{
                "message": response
            }
        }
    except:
        return {"status": "false", "message": "Error response."}

@app.post("/ryuzaki/chatgpt-model")
def chatgpt_model(
    query: str=None,
    model_id: int=1,
    is_models: bool=True
):
    try:
        response = RendyDevChat(query).get_response_model(model_id=model_id, is_models=is_models)
        return {
            "status": "true",
            "randydev":{
                "message": response
            }
        }
    except:
        return {"status": "false", "message": "Error response."}

async def get_data(username):
    base_msg = ""
    async with AsyncClient() as gpx:
        req = (await gpx.get(f"https://api.github.com/users/{username}")).json()
        try:
            avatar = req["avatar_url"]
            twitter = req['twitter_username']
            base_msg += "**❆ Gitub Information ❆** \n\n"
            base_msg += f"**Profile Url:** {req['html_url']} \n"
            base_msg += f"**Name:** `{req['name']}` \n"
            base_msg += f"**Username:** `{req['login']}` \n"
            base_msg += f"**User ID:** `{req['id']}` \n"
            base_msg += f"**Location:** `{req['location']}` \n"
            base_msg += f"**Company:** `{req['company']}` \n"
            base_msg += f"**Blog:** `{req['name']}` \n"
            base_msg += f"**Twitter:** `{f'https://twitter.com/{twitter}' if twitter else 'None'}` \n"
            base_msg += f"**Bio:** `{req['bio']}` \n"
            base_msg += f"**Public Repos:** `{req['public_repos']}` \n"
            base_msg += f"**Public Gists:** `{req['public_gists']}` \n"
            base_msg += f"**Followers:** `{req['followers']}` \n"
            base_msg += f"**Following:** `{req['following']}` \n"
            base_msg += f"**Created At:** `{req['created_at']}` \n"
            base_msg += f"**Update At:** `{req['updated_at']}` \n"
            return [base_msg, avatar]
        except Exception as e:
            base_msg += f"**An error occured while parsing the data!** \n\n**Traceback:** \n `{e}` \n\n`Make sure that you've sent the command with the correct username!`"
            return [base_msg, "https://telegra.ph//file/32f69c18190666ea96553.jpg"]

@app.get("/ryuzaki/github")
async def github(username: str=None):
    try:
        details = await get_data(username)
        return {
            "status": "true",
            "randydev":{
                "avatar": details[1],
                "results": details[0]
            }
        }
    except:
        return {"status": "false", "message": "Error response."}

@app.get("/ryuzaki/webshot")
def webshot(
    url: str=None,
    quality: str="1920x1080",
    type_mine: str="JPEG",
    pixels: str="1024",
    cast: str="Z100"
):
    try:
        required_url = f"https://mini.s-shot.ru/{quality}/{type_mine}/{pixels}/{cast}/?{url}"
        return {
            "status": "true",
            "randydev":{
                "image_url": required_url
            }
        }
    except:
        return {"status": "false", "message": "Error response."}

@app.get("/ryuzaki/chatbot")
def chatbot(
    query: str=None,
    user_id: int=None,
    bot_name: str=None,
    bot_username: str=None
):
    api_url = b64decode("aHR0cHM6Ly9hcGkuc2Fmb25lLmRldi9jaGF0Ym90").decode("utf-8")
    params = {
        "query": query,
        "user_id": user_id,
        "bot_name": bot_name,
        "bot_master": bot_username
    }
    x = requests.get(f"{api_url}", params=params)
    if x.status_code != 200:
        return "Error api request"
    try:
        y = x.json()
        response = y["response"]
        return {
            "status": "true",
            "randydev":{
                "message": response
            }
        }
    except:
        return {"status": "false", "message": "Error response."}

@app.get("/ryuzaki/waifu")
def waifu_pics(
    types: str="sfw",
    category: str="neko"
):
    waifu_api = f"{SOURCR_WAIFU_URL}/{types}"
    waifu_param = f"{waifu_api}/{category}"
    
    response = requests.get(waifu_param)
    
    if response.status_code != 200:
        return "Sorry, there was an error processing your request. Please try again later"
    data_waifu = response.json()
    try:
        waifu_image_url = data_waifu["url"]
    except Exception as e:
        return f"Error request {e}"
    if waifu_image_url:
        try:
            return {
                "status": "true",
                "randydev":{
                    "image_url": waifu_image_url
                }
            }
        except:
            return {"status": "false", "message": "Error response"}
    else:
        return {"status": "false", "message": "Error response."}

@app.get("/ryuzaki/rayso")
def make_rayso(
    code=None,
    title: str="Ryuzaki Dev",
    theme: str=None,
    setlang: str="en",
    auto_translate: bool=None,
    ryuzaki_dark: bool=None
):
    trans = SyncTranslator()
    api_url = b64decode("aHR0cHM6Ly9hcGkuc2Fmb25lLm1lL3JheXNv").decode("utf-8")
    if auto_translate:
        source = trans.detect(code)
        translation = trans(code, sourcelang=source, targetlang=setlang)
        code = translation.text
    else:
        code = code
    if ryuzaki_dark:
        x = requests.post(
            f"{api_url}",
            json={
                "code": code,
                "title": title,
                "theme": theme,
                "darkMode": True
            }
        )
        if x.status_code != 200:
            return "Error api Gay"
        data = x.json()
        try:
            image_data = base64.b64decode(data["image"])
            return {
                "status": "true",
                "data":{
                    "image": image_data
                }
            }
        except:
            return {"status": "false", "message": "Error response"}
    else:
        x = requests.post(
            f"{api_url}",
            json={
                "code": code,
                "title": title,
                "theme": theme,
                "darkMode": False
            }
        )
        if x.status_code != 200:
            return "Error api Gay"
        data = x.json()
        try:
            image_data = base64.b64decode(data["image"])
            return {
                "status": "true",
                "data":{
                    "image": image_data
                }
            }
        except:
            return {"status": "false", "message": "Error response"}

@app.get("/ryuzaki/ipcheck")
def whois_ip_address(ip_address: str=None):
    apikey = kc("M0QwN0UyRUFBRjU1OTQwQUY0NDczNEMzRjJBQzdDMUE=").decode("utf-8")
    location_link = "https"
    location_api = "api.ip2location.io"
    location_key = f"key={apikey}"
    location_search = f"ip={ip_address}"
    location_param = (
        f"{location_link}://{location_api}/?{location_key}&{location_search}"
    )
    response = requests.get(location_param)
    if response.status_code != 200:
        return "Sorry, there was an error processing your request. Please try again later"
    data_location = response.json()
    try:
        location_ip = data_location["ip"]
        location_code = data_location["country_code"]
        location_name = data_location["country_name"]
        location_region = data_location["region_name"]
        location_city = data_location["city_name"]
        location_zip = data_location["zip_code"]
        location_zone = data_location["time_zone"]
        location_card = data_location["as"]
    except Exception as e:
        return f"error {e}"
    if (
        location_ip
        and location_code
        and location_name
        and location_region
        and location_city
        and location_zip
        and location_zone
        and location_card
    ):
        return {
            "ip_address": location_ip,
            "country_code": location_code,
            "region_name": location_region,
            "city_name": location_city,
            "zip_code": location_zip,
            "time_zone": location_zone,
            "as": location_card
        }
    else:
        return {"status": "false", "message": "Invalid ip address"}

@app.get("/ryuzaki/tiktok_douyin")
def tiktok_douyin(tiktok_url: str=None):
    response = requests.get(f"{SOURCR_TIKTOK_WTF_URL}={tiktok_url}")
    if response.status_code != 200:
        return "Error request:"
    try:
        download_video = response.json()["aweme_list"][0]["video"]["play_addr"]["url_list"][0]
        download_audio = response.json()["aweme_list"][0]["music"]["play_url"]["url_list"][0]
        description = response.json()["aweme_list"][0]["desc"]
        author = response.json()["aweme_list"][0]["author"]["nickname"]
        request = response.json()["aweme_list"][0]["author"]["signature"]
        return {
            "status": "true",
            "randydev": {
                "video_url": download_video,
                "music_url": download_audio,
                "description": description,
                "author": author,
                "request": request
            }
        }
    except:
        return {"status": "false", "message": "Error request"}

@app.get("/ryuzaki/tiktok")
def tiktok_downloader(tiktok_url: Union[str, None] = None, only_video: bool=None):
    api_devs = SOURCR_TIKTOK_TECH_URL
    parameter = f"tiktok?url={tiktok_url}"
    api_url = f"{api_devs}/{parameter}"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        return "Error: Unable to fetch data from the TikTok API"
    try:
        results = response.json()
        caption = results.get("result", {}).get("desc", "")
        if only_video:
            video_url = results.get("result", {}).get("withoutWaterMarkVideo", "")
            if video_url:
                return {
                    "download_url": video_url,
                    "caption": caption
                }
        else:
            music_mp3 = results.get("result", {}).get("music", "")
            if music_mp3:
                return {
                    "music_url": music_mp3,
                    "caption": caption
                }
        return "Error: TikTok data not found or unsupported format"
    except:
        return {"status": "false", "message": "Invalid Link"}
        
@app.get("/ryuzaki/mediafire")
def mediafire(link: Union[str, None] = None):
  try:
    down_link = str(link)
    mid = down_link.split('/', 5)
    if mid[3] == "view":
      mid[3] = "file"
      down_link = '/'.join(mid)
      print(down_link)
    r = requests.get(down_link)
    soup = BeautifulSoup(r.content, "html.parser")
    a_href = soup.find("a", {"class": "input popsok"}).get("href")
    a = str(a_href)
    id = link.split('/', 5)[4]
    a_byte = soup.find("a", {"class": "input popsok"}).get_text()
    a_name = soup.find("div", {"class": "dl-btn-label"}).get_text()
    details = soup.find("ul", {"class": "details"})
    li_items = details.find_all('li')[1]
    some = li_items.find_all("span")[0].get_text().split()
    dat = list(some)
    down = a_byte.replace(" ", "").strip()
    time = dat[1]
    date = dat[0]
    byte = down.split("(", 1)[1].split(")", 1)[0]
    name = a_name.replace(" ", "").strip()
    return {
      "status": "true",
      "data": {
        "file": {
          "url": {
            'directDownload': a,
            "original": link,
          },
          "metadata": {
            "id": id,
            "name": name,
            "size": {
              "readable": byte
            },
            "DateAndTime": {
              "time": time,
              "date": date
            }
          }
        }
      }
    }

  except:
    return "{'status': 'false', 'message': 'Invalid Link'}"


@app.get("/ryuzaki/gdrive")
def gdrive(link: Union[str, None] = None):
  try:
    down = link.split('/', 6)
    url = f'https://drive.google.com/uc?export=download&id={down[5]}'
    session = requests.Session()

    response = session.get(url, stream=True)
    headers = response.headers
    content_disp = headers.get('content-disposition')
    filename = None
    if content_disp:
      match = re.search(r'filename="(.+)"', content_disp)
      if match:
        filename = match.group(1)

    content_length = headers.get('content-length')
    last_modified = headers.get('last-modified')
    content_type = headers.get('content-type')

    return {
      "status": "true",
      "data": {
        "file": {
          "url": {
            'directDownload': url,
            "original": link,
          },
          "metadata": {
            "id":
            down[5],
            "name":
            filename if filename else 'No filename provided by the server.',
            "size": {
              "readable":
              f'{round(int(content_length) / (1024 * 1024), 2)} MB' if
              content_length else 'No content length provided by the server.',
              "type":
              content_type
              if content_type else 'No content type provided by the server.'
            },
            "DateAndTime":
            last_modified if last_modified else
            'No last modified date provided by the server.',
          }
        }
      }
    }

  except:
    return "{'status': 'false', 'message': 'Invalid Link'}"

@app.get("/ryuzaki/anonfiles")
def anonfiles(link: Union[str, None] = None):
  try:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    a_href = soup.find("a", {"id": "download-url"}).get("href")
    a = str(a_href)
    id = link.split('/', 4)[3]
    jsondata = requests.get(
      f'https://api.anonfiles.com/v2/file/{id}/info').json()
    jsondata['data']['file']['url']['directDownload'] = a
    del jsondata['data']['file']['url']['full']

    return jsondata
  except:
    return "{'status': 'false', 'message': 'Invalid Link'}"

@app.get("/ryuzaki/filechan")
def filechan(link: Union[str, None] = None):
  try:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    a_href = soup.find("a", {"id": "download-url"}).get("href")
    a = str(a_href)
    id = link.split('/', 4)[3]
    jsondata = requests.get(
      f'https://api.filechan.org/v2/file/{id}/info').json()
    jsondata['data']['file']['url']['directDownload'] = a
    del jsondata['data']['file']['url']['full']

    return jsondata
  except:
    return "{'status': 'false', 'message': 'Invalid Link'}"

@app.get("/ryuzaki/letsupload")
def letsupload(link: Union[str, None] = None):
  try:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    a_href = soup.find("a", {"id": "download-url"}).get("href")
    a = str(a_href)
    id = link.split('/', 4)[3]
    jsondata = requests.get(
      f'https://api.letsupload.cc/v2/file/{id}/info').json()
    jsondata['data']['file']['url']['directDownload'] = a
    del jsondata['data']['file']['url']['full']

    return jsondata
  except:
    return "{'status': 'false', 'message': 'Invalid Link'}"

@app.get("/ryuzaki/megaupload")
def megaupload(link: Union[str, None] = None):
  try:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    a_href = soup.find("a", {"id": "download-url"}).get("href")
    a = str(a_href)
    id = link.split('/', 4)[3]
    jsondata = requests.get(
      f'https://api.megaupload.nz/v2/file/{id}/info').json()
    jsondata['data']['file']['url']['directDownload'] = a
    del jsondata['data']['file']['url']['full']

    return jsondata
  except:
    return "{'status': 'false', 'message': 'Invalid Link'}"

@app.get("/ryuzaki/myfile")
def myfile(link: Union[str, None] = None):
  try:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    a_href = soup.find("a", {"id": "download-url"}).get("href")
    a = str(a_href)
    id = link.split('/', 4)[3]
    jsondata = requests.get(
      f'https://api.myfile.is/v2/file/{id}/info').json()
    jsondata['data']['file']['url']['directDownload'] = a
    del jsondata['data']['file']['url']['full']

    return jsondata
  except:
    return "{'status': 'false', 'message': 'Invalid Link'}"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
