#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from bot import Bot
from config import *
from database.database import db

@Bot.on_callback_query(filters.regex(r"^(help|about|home|premium|close|rfs_ch_|rfs_toggle_|fsub_back|set_|remove_)"))
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    user = query.from_user

    if data == "help":
        try:
            selected_image = random.choice(RANDOM_IMAGES)
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='home'),
                 InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data='close')]
            ])
            caption = HELP_TXT.format(
                first=user.first_name,
                last=user.last_name if user.last_name else "",
                username=None if not user.username else '@' + user.username,
                mention=user.mention,
                id=user.id
            )
            await query.message.edit_media(
                media=InputMediaPhoto(media=selected_image, caption=caption),
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"ᴇʀʀᴏʀ ɪɴ ʜᴇʟᴘ ᴄᴀʟʟʙᴀᴄᴋ: {e}")
            await query.message.edit_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴜᴘᴅᴀᴛɪɴɢ ᴛʜᴇ ʜᴇʟᴘ ᴍᴇssᴀɢᴇ.")
        await query.answer()

    elif data == "about":
        try:
            selected_image = random.choice(RANDOM_IMAGES)
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='home'),
                 InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data='close')]
            ])
            caption = ABOUT_TXT.format(
                first=user.first_name,
                last=user.last_name if user.last_name else "",
                username=None if not user.username else '@' + user.username,
                mention=user.mention,
                id=user.id
            )
            await query.message.edit_media(
                media=InputMediaPhoto(media=selected_image, caption=caption),
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"ᴇʀʀᴏʀ ɪɴ ᴀʙᴏᴜᴛ ᴄᴀʟʟʙᴀᴄᴋ: {e}")
            await query.message.edit_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴜᴘᴅᴀᴛɪɴɢ ᴛʜᴇ ᴀʙᴏᴜᴛ ᴍᴇssᴀɢᴇ.")
        await query.answer()

    elif data == "home":
        try:
            selected_image = random.choice(RANDOM_IMAGES)
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("ᴍᴏʀᴇ ᴄʜᴀɴɴᴇʟs", url="https://t.me/Anime_Lord_List")],
                [InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"), InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help")]
            ])
            caption = START_MSG.format(
                first=user.first_name,
                last=user.last_name if user.last_name else "",
                username=None if not user.username else '@' + user.username,
                mention=user.mention,
                id=user.id
            )
            await query.message.edit_media(
                media=InputMediaPhoto(media=selected_image, caption=caption),
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"ᴇʀʀᴏʀ ɪɴ ʜᴏᴍᴇ ᴄᴀʟʟʙᴀᴄᴋ: {e}")
            await query.message.edit_text("ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ʀᴇᴛᴜʜʀɴɪɴɢ ᴛᴏ ʜᴏᴍᴇ.")
        await query.answer()

    elif data == "premium":
        await query.message.delete()
        await client.send_photo(
            chat_id=query.message.chat.id,
            photo=QR_PIC,
            caption=(
                f"👋 {query.from_user.username if query.from_user.username else 'user'}\n\n"
                f"🎖️ ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs :\n\n"
                f"● {PRICE1}  ғᴏʀ 0 ᴅᴀʏs ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n"
                f"● {PRICE2}  ғᴏʀ 1 ᴍᴏɴᴛʜ ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n"
                f"● {PRICE3}  ғᴏʀ 3 ᴍᴏɴᴛʜs ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n"
                f"● {PRICE4}  ғᴏʀ 6 ᴍᴏɴᴛʜs ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n"
                f"● {PRICE5}  ғᴏʀ 1 ʏᴇᴀʀ ᴘʀɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ\n\n\n"
                f"💵 ᴀsᴋ ᴜᴘɪ ɪᴅ ᴛᴏ ᴀᴅᴍɪɴ ᴀɴᴅ ᴘᴀʏ ᴛʜᴇʀᴇ -  <code>{UPI_ID}</code>\n\n\n"
                f"♻️ ᴘᴀʏᴍᴇɴᴛ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ɪɴsᴛᴀɴᴛ ᴍᴇᴍʙᴇʀsʜɪᴘ \n\n\n"
                f"‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ & ɪғ ᴀɴʏᴏɴᴇ ᴡᴀɴᴛ ᴄᴜsᴛᴏᴍ ᴛɪᴍᴇ ᴍᴇᴍʙᴇʀsʜɪᴘ ᴛʜᴇɴ ᴀsᴋ ᴀᴅᴍɪɴ"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "ᴀᴅᴍɪɴ 24/7", url=(SCREENSHOT_URL)
                        )
                    ],
                    [InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")],
                ]
            )
        )
        await query.answer()

    elif data == "close":
        try:
            # Delete the callback message and the original command message if it exists
            await query.message.delete()
            if query.message.reply_to_message:
                await query.message.reply_to_message.delete()
        except Exception as e:
            print(f"ᴇʀʀᴏʀ ɪɴ ᴄʟᴏsᴇ ᴄᴀʟʟʙᴀᴄᴋ: {e}")
        await query.answer()

    elif data.startswith("rfs_ch_"):
        cid = int(data.split("_")[2])
        try:
            chat = await client.get_chat(cid)
            mode = await db.get_channel_mode(cid)
            status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
            new_mode = "off" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'off' if mode == 'on' else 'on'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"ᴄʜᴀɴɴᴇʟ: {chat.title}\nᴄᴜʀʀᴇɴᴛ ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ: {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception:
            await query.answer("ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ᴄʜᴀɴɴᴇʟ ɪɴғᴏ", show_alert=True)

    elif data.startswith("rfs_toggle_"):
        cid, action = data.split("_")[2:]
        cid = int(cid)
        mode = "on" if action == "on" else "off"
        await db.set_channel_mode(cid, mode)
        await query.answer(f"ғᴏʀᴄᴇ-sᴜʙ sᴇᴛ ᴛᴏ {'on' if mode == 'on' else 'off'}")
        chat = await client.get_chat(cid)
        status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
        new_mode = "off" if mode == "on" else "on"
        buttons = [
            [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'off' if mode == 'on' else 'on'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="fsub_back")]
        ]
        await query.message.edit_text(
            f"ᴄʜᴀɴɴᴇʟ: {chat.title}\nᴄᴜʀʀᴇɴᴛ ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ: {status}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "fsub_back":
        channels = await db.show_channels()
        buttons = []
        for cid in channels:
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
            except:
                continue
        await query.message.edit_text(
            "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await query.answer()

    elif data.startswith("set_"):
        type = data.split("_")[1]
        await db.set_temp_state(query.message.chat.id, f"set_{type}")
        await query.message.reply_text(f"ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴍᴇ ᴛʜᴇ {type} ɪᴍᴀɢᴇ.")
        await query.answer()

    elif data.startswith("remove_"):
        type = data.split("_")[1]
        images = await db.get_images(type)
        if not images:
            await query.message.reply_text(f"ᴛʜᴇʀᴇ ᴀʀᴇ ɴᴏ {type} ɪᴍᴀɢᴇs sᴇᴛ.")
        else:
            nums = list(range(1, len(images) + 1))
            text = f"ᴄᴜʀʀᴇɴᴛ {type} ɪᴍᴀɢᴇs: {', '.join(map(str, nums))}\nᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀ sɪɴɢʟᴇ ɪᴍᴀɢᴇ, ᴜsᴇ /rev_{type} <number>\nᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀʟʟ, ᴜsᴇ /rev_all_{type}"
            await query.message.reply_text(text)
        await query.answer()


#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
