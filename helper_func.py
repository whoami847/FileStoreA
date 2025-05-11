#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.

import base64
import re
import asyncio
import time
import logging
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import *
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from shortzy import Shortzy
from pyrogram.errors import FloodWait
from database.database import *

logger = logging.getLogger(__name__)

async def check_admin(filter, client, update):
    try:
        user_id = update.from_user.id       
        is_admin = user_id == OWNER_ID or await db.admin_exist(user_id)
        if not is_admin:
            logger.warning(f"User {user_id} attempted admin action without permission")
        return is_admin
    except Exception as e:
        logger.error(f"Exception in check_admin for user {user_id}: {e}")
        return False

async def is_subscribed(client, user_id):
    channel_ids = await db.show_channels()

    if not channel_ids:
        return True

    if user_id == OWNER_ID:
        return True

    for cid in channel_ids:
        if not await is_sub(client, user_id, cid):
            mode = await db.get_channel_mode(cid)
            if mode == "on":
                await asyncio.sleep(2)
                if await is_sub(client, user_id, cid):
                    continue
            logger.info(f"User {user_id} not subscribed to channel {cid}")
            return False

    return True

async def is_sub(client, user_id, channel_id):
    try:
        member = await client.get_chat_member(channel_id, user_id)
        status = member.status
        logger.debug(f"User {user_id} in channel {channel_id} with status {status}")
        return status in {
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER
        }
    except UserNotParticipant:
        mode = await db.get_channel_mode(channel_id)
        if mode == "on":
            exists = await db.req_user_exist(channel_id, user_id)
            logger.debug(f"User {user_id} join request for channel {channel_id}: {exists}")
            return exists
        logger.info(f"User {user_id} not subscribed to channel {channel_id}")
        return False
    except Exception as e:
        logger.error(f"Error in is_sub for user {user_id} in channel {channel_id}: {e}")
        return False

async def encode(string):
    return base64.urlsafe_b64encode(string.encode()).decode().strip("=")

async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode()
    return base64.urlsafe_b64decode(base64_bytes).decode()

async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    max_retries = 3

    while total_messages < len(message_ids):
        temp_ids = message_ids[total_messages:total_messages + 200]
        for attempt in range(max_retries):
            try:
                msgs = await client.get_messages(client.db_channel.id, temp_ids)
                messages.extend(msgs)
                break
            except FloodWait as e:
                logger.warning(f"FloodWait error: Waiting for {e.x} seconds")
                await asyncio.sleep(e.x)
                if attempt == max_retries - 1:
                    logger.error(f"Max retries reached for message IDs {temp_ids}")
            except Exception as e:
                logger.error(f"Error fetching messages {temp_ids}: {e}")
                break
        total_messages += len(temp_ids)

    return messages

async def get_message_id(client, message):
    if message.forward_from_chat:
        if message.forward_from_chat.id == client.db_channel.id:
            return message.forward_from_message_id
        return 0
    if message.forward_sender_name:
        return 0
    if message.text:
        pattern = r"https://t.me/(?:c/)?(.*)/(\d+)"
        matches = re.match(pattern, message.text)
        if not matches:
            return 0
        channel_id, msg_id = matches.groups()
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(client.db_channel.id):
                return int(msg_id)
        else:
            if channel_id == client.db_channel.username:
                return int(msg_id)
    return 0

def get_readable_time(seconds: int) -> str:
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    for i in range(4):
        if i < 3:
            seconds, remainder = divmod(seconds, 60)
        else:
            seconds, remainder = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(f"{int(remainder)}{time_suffix_list[i]}")
    return ":".join(reversed(time_list)) or "0s"

def get_exp_time(seconds):
    periods = [('days', 86400), ('hours', 3600), ('mins', 60), ('secs', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)} {period_name} '
    return result.strip()

async def get_shortlink(url, api, link):
    try:
        shortzy = Shortzy(api_key=api, base_site=url)
        short_link = await shortzy.convert(link)
        return short_link
    except Exception as e:
        logger.error(f"Error generating shortlink for {link}: {e}")
        return link

subscribed = filters.create(is_subscribed)
admin = filters.create(check_admin)

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#