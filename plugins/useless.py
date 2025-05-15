#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import os
import random
import sys
import time
import logging
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatInviteLink, ChatPrivileges
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

# Set up logging for this module
logger = logging.getLogger(__name__)

#=====================================================================================##

@Bot.on_message(filters.command('stats') & admin)
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))

#=====================================================================================##

WAIT_MSG = "<b>ᴡᴏʀᴋɪɴɢ....</b>"

#=====================================================================================##

@Bot.on_message(filters.command('users') & filters.private & admin)
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await db.full_userbase()
    await msg.edit(f"{len(users)} ᴜꜱᴇʀꜱ ᴀʀᴇ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ")

#=====================================================================================##

# AUTO-DELETE SETTINGS

# Function to show the auto-delete settings with inline buttons
async def show_auto_delete_settings(client: Bot, chat_id: int, message_id: int = None):
    auto_delete_mode = await db.get_auto_delete_mode()
    delete_timer = await db.get_del_timer()
    
    mode_status = "Enabled ✅" if auto_delete_mode else "Disabled ❌"
    timer_text = get_readable_time(delete_timer)

    settings_text = (
        "» <b>AUTO DELETE SETTINGS</b>\n\n"
        f"» <b>AUTO DELETE MODE:</b> {mode_status}\n"
        f"» <b>DELETE TIMER:</b> {timer_text}\n\n"
        "<b>CLICK BELOW BUTTONS TO CHANGE SETTINGS</b>"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• ᴅɪsᴀʙʟᴇᴅ ❌" if auto_delete_mode else "• ᴇɴᴀʙʟᴇᴅ ✅", callback_data="auto_toggle"),
                InlineKeyboardButton("• sᴇᴛ ᴛɪᴍᴇʀ •", callback_data="auto_set_timer")
            ],
            [
                InlineKeyboardButton("• ʀᴇғʀᴇsʜ", callback_data="auto_refresh"),
                InlineKeyboardButton("ʙᴀᴄᴋ •", callback_data="auto_back")
            ]
        ]
    )

    if message_id:
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=settings_text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    else:
        await client.send_message(
            chat_id=chat_id,
            text=settings_text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

@Bot.on_message(filters.private & filters.command('auto_delete') & admin)
async def auto_delete_settings(client: Bot, message: Message):
    await show_auto_delete_settings(client, message.chat.id)

@Bot.on_callback_query(filters.regex(r"^auto_"))
async def auto_delete_callback(client: Bot, callback: CallbackQuery):
    data = callback.data
    chat_id = callback.message.chat.id

    if data == "auto_toggle":
        current_mode = await db.get_auto_delete_mode()
        new_mode = not current_mode
        await db.set_auto_delete_mode(new_mode)
        await show_auto_delete_settings(client, chat_id, callback.message.id)
        await callback.answer(f"Auto Delete Mode {'Enabled' if new_mode else 'Disabled'}!")
    
    elif data == "auto_set_timer":
        # Set a state to indicate that we are expecting a timer input
        await db.set_temp_state(chat_id, "awaiting_timer_input")
        logger.info(f"Set state to 'awaiting_timer_input' for chat {chat_id}")
        await callback.message.reply(
            "<b>Please provide the duration in seconds for the delete timer.</b>\n"
            "Example: 300 (for 5 minutes)",
            parse_mode=ParseMode.HTML
        )
        await callback.answer("Enter the duration!")
    
    elif data == "auto_refresh":
        await show_auto_delete_settings(client, chat_id, callback.message.id)
        await callback.answer("Settings refreshed!")
    
    elif data == "auto_back":
        await callback.message.delete()
        await callback.answer("Back to previous menu!")

@Bot.on_message(filters.private & filters.regex(r"^\d+$") & admin)
async def set_timer(client: Bot, message: Message):
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    
    logger.info(f"Received numeric input: {message.text} from chat {chat_id}, current state: {state}")

    # Only process the input if the state is "awaiting_timer_input"
    if state == "awaiting_timer_input":
        try:
            duration = int(message.text)
            await db.set_del_timer(duration)
            await message.reply(f"<b>Delete Timer has been set to {get_readable_time(duration)}.</b>", parse_mode=ParseMode.HTML)
            logger.info(f"Set delete timer to {duration} seconds for chat {chat_id}")
            # Clear the state after processing
            await db.set_temp_state(chat_id, "")
        except ValueError:
            await message.reply("<b>Please provide a valid duration in seconds.</b>", parse_mode=ParseMode.HTML)
            logger.error(f"Invalid duration input: {message.text} from chat {chat_id}")
    else:
        logger.info(f"Ignoring numeric input: {message.text} as state is not 'awaiting_timer_input' for chat {chat_id}")

#=====================================================================================##

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
