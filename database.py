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

import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_URL = os.environ["MONGO_URL"]

client_mongo = MongoClient(MONGO_URL)
db = client_mongo["tiktokbot"]
collection = db["users"]

RAMDOM_STATUS = [
    "civilian",
    "wanted",
    "undercover",
    "rogue_agent",
    "innocent",
    "fugitive",
    "covert_operator"
]

def remove_sibyl_system_banned(user_id):
    update_doc = {
        "sibyl_ban": None,
        "reason_sibyl": None,
        "is_banned_sibly": None,
        "date_joined_sib": None,
        "sibyl_userid": None
    }
    return collection.update_one({"user_id": user_id}, {"$unset": update_doc}, upsert=True)

def new_sibyl_system_banned(user_id, name, reason, date_joined):
    update_doc = {
        "sibyl_ban": name,
        "reason_sibyl": reason,
        "is_banned_sibly": True,
        "date_joined_sib": date_joined,
        "sibyl_userid": user_id
    }
    return collection.update_one({"user_id": user_id}, {"$set": update_doc}, upsert=True)

def get_sibyl_system_banned(user_id):
    user = collection.find_one({"user_id": user_id})
    if user:
        sibyl_name = user.get("sibyl_ban")
        reason = user.get("reason_sibyl")
        is_banned = user.get("is_banned_sibly")
        date_joined = user.get("date_joined_sib")
        sibyl_user_id = user.get("sibyl_userid")
        return sibyl_name, reason, is_banned, date_joined, sibyl_user_id
    else:
        return None

def get_all_banned():
    banned_users = []

    users = collection.find({})

    for user_id in users:
        reason = user_id.get("reason_sibyl")
        user_id = user_id.get("sibyl_userid")
        banned_users.append({"user_id": user_id, "reason": reason})
    return banned_users

def get_all_api_keys():
    user = collection.find({})
    api_keys = []
    for x in user:
        api_key = x.get("ryuzaki_api_key")
        if api_key:
            api_keys.append(api_key)
    return api_keys
