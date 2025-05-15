import asyncio
import os
import random
import sys
import time
from datetime import datetime, timedelta
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

# Auto Delete Settings Inline Keyboard
def get_auto_delete_settings_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Disabled ❌", callback_data="auto_delete_off"),
            InlineKeyboardButton("Set Timer ⏰", callback_data="set_timer")
        ],
        [
            InlineKeyboardButton("Refresh 🔄", callback_data="refresh"),
            InlineKeyboardButton("Back ⬅️", callback_data="back")
        ]
    ])

# Show Auto Delete Settings with Image
@Bot.on_message(filters.private & filters.command('auto_delete') & admin)
async def auto_delete_settings(client: Bot, message: Message):
    duration = await db.get_del_timer()
    if duration:
        duration_str = f"{duration // 60} Minutes" if duration % 60 == 0 else f"{duration} Seconds"
    else:
        duration_str = "Not Set"
    
    await message.reply_photo(
        photo="https://envs.sh/ozr.jpg",
        caption=f"<b>AUTO DELETE SETTINGS</b>\n"
                f"> AUTO DELETE MODE: {'ENABLED ✅' if duration else 'DISABLED ❌'}\n"
                f"> DELETE TIMER: {duration_str}\n\n"
                f"Click below buttons to change settings",
        reply_markup=get_auto_delete_settings_keyboard()
    )

# Handle Callback Queries
@Bot.on_callback_query(filters.private & admin)
async def handle_callback(client: Bot, callback_query: CallbackQuery):
    data = callback_query.data
    message = callback_query.message

    if data == "auto_delete_off":
        await db.set_del_timer(0)  # Disable by setting timer to 0
        await message.edit_caption(
            caption=f"<b>AUTO DELETE SETTINGS</b>\n"
                    f"> AUTO DELETE MODE: DISABLED ❌\n"
                    f"> DELETE TIMER: Not Set\n\n"
                    f"Click below buttons to change settings",
            reply_markup=get_auto_delete_settings_keyboard()
        )

    elif data == "set_timer":
        await message.edit_caption(
            caption="<b>Enter new delete timer in minutes (e.g., 5 for 5 minutes):</b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back ⬅️", callback_data="back")]])
        )
        await client.listen(message.chat.id, filters=filters.text & admin, timeout=30)

    elif data == "refresh":
        duration = await db.get_del_timer()
        duration_str = f"{duration // 60} Minutes" if duration % 60 == 0 else f"{duration} Seconds" if duration else "Not Set"
        await message.edit_caption(
            caption=f"<b>AUTO DELETE SETTINGS</b>\n"
                    f"> AUTO DELETE MODE: {'ENABLED ✅' if duration else 'DISABLED ❌'}\n"
                    f"> DELETE TIMER: {duration_str}\n\n"
                    f"Click below buttons to change settings",
            reply_markup=get_auto_delete_settings_keyboard()
        )

    elif data == "back":
        await message.delete()
        await auto_delete_settings(client, message)

    # Handle timer input
    elif data.startswith("set_timer_value_"):
        try:
            timer_value = int(data.split("_")[2])
            await db.set_del_timer(timer_value * 60)  # Convert minutes to seconds
            duration_str = f"{timer_value} Minutes"
            await message.edit_caption(
                caption=f"<b>AUTO DELETE SETTINGS</b>\n"
                        f"> AUTO DELETE MODE: ENABLED ✅\n"
                        f"> DELETE TIMER: {duration_str}\n\n"
                        f"Click below buttons to change settings",
                reply_markup=get_auto_delete_settings_keyboard()
            )
        except ValueError:
            await message.edit_caption("<b>Invalid input! Please enter a valid number.</b>")

# Listen for timer input
@Bot.on_message(filters.private & filters.text & admin)
async def set_timer_input(client: Bot, message: Message):
    try:
        timer_value = int(message.text)
        await db.set_del_timer(timer_value * 60)  # Convert minutes to seconds
        duration_str = f"{timer_value} Minutes"
        await message.reply_photo(
            photo="https://envs.sh/ozr.jpg",
            caption=f"<b>AUTO DELETE SETTINGS</b>\n"
                    f"> AUTO DELETE MODE: ENABLED ✅\n"
                    f"> DELETE TIMER: {duration_str}\n\n"
                    f"Click below buttons to change settings",
            reply_markup=get_auto_delete_settings_keyboard()
        )
    except ValueError:
        await message.reply("<b>Invalid input! Please enter a valid number in minutes.</b>")

# Existing commands (modified for consistency)
@Bot.on_message(filters.private & filters.command('dlt_time') & admin)
async def set_delete_time(client: Bot, message: Message):
    await message.reply("<b>Use /auto_delete command to set delete timer interactively.</b>")

@Bot.on_message(filters.private & filters.command('check_dlt_time') & admin)
async def check_delete_time(client: Bot, message: Message):
    duration = await db.get_del_timer()
    duration_str = f"{duration // 60} Minutes" if duration % 60 == 0 else f"{duration} Seconds" if duration else "Not Set"
    await message.reply(
        f"<b>CURRENT DELETE TIMER IS SET TO {duration_str}.</b>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Change Settings", callback_data="auto_delete")]])
    )
