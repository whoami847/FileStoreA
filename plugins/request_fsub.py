#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import os
import random
import sys
import time
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatMemberUpdated, ChatPermissions
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, InviteHashEmpty, ChatAdminRequired, PeerIdInvalid, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

@Bot.on_message(filters.command('fsub_mode') & filters.private & admin)
async def change_force_sub_mode(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    channels = await db.show_channels()

    if not channels:
        return await temp.edit("<b>❌ ɴᴏ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ғᴏᴜɴᴅ.</b>")

    buttons = []
    for ch_id in channels:
        try:
            chat = await client.get_chat(ch_id)
            mode = await db.get_channel_mode(ch_id)
            status = "🟢" if mode == "on" else "🔴"
            title = f"{status} {chat.title}"
            buttons.append([InlineKeyboardButton(title, callback_data=f"rfs_ch_{ch_id}")])
        except:
            buttons.append([InlineKeyboardButton(f"⚠️ {ch_id} (ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ)", callback_data=f"rfs_ch_{ch_id}")])

    buttons.append([InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")])

    await temp.edit(
        "<b>⚡ sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )

@Bot.on_chat_member_updated()
async def handle_Chatmembers(client, chat_member_updated: ChatMemberUpdated):    
    chat_id = chat_member_updated.chat.id

    if await db.reqChannel_exist(chat_id):
        old_member = chat_member_updated.old_chat_member

        if not old_member:
            return

        if old_member.status == ChatMemberStatus.MEMBER:
            user_id = old_member.user.id

            if await db.req_user_exist(chat_id, user_id):
                await db.del_req_user(chat_id, user_id)

@Bot.on_chat_join_request()
async def handle_join_request(client, chat_join_request):
    chat_id = chat_join_request.chat.id
    user_id = chat_join_request.from_user.id

    if await db.reqChannel_exist(chat_id):
        if not await db.req_user_exist(chat_id, user_id):
            await db.req_user(chat_id, user_id)

@Bot.on_message(filters.command('addchnl') & filters.private & admin)
async def add_force_sub(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    args = message.text.split(maxsplit=1)

    if len(args) != 2:
        buttons = [[InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")]]
        return await temp.edit(
            "<b>ᴜꜱᴀɢᴇ:</b> <code>/addchnl -100XXXXXXXXXX</code>\n<b>ᴀᴅᴅ ᴏɴʟʏ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ ᴀᴛ ᴀ ᴛɪᴍᴇ.</b>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    try:
        channel_id = int(args[1])
    except ValueError:
        return await temp.edit("<b>❌ ɪɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ ɪᴅ!</b>")

    all_channels = await db.show_channels()
    channel_ids_only = [cid if isinstance(cid, int) else cid[0] for cid in all_channels]
    if channel_id in channel_ids_only:
        return await temp.edit(f"<b>ᴄʜᴀɴɴᴇʟ ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs:</b> <code>{channel_id}</code>")

    try:
        # Attempt to get chat information
        chat = await client.get_chat(channel_id)
        if chat.type != ChatType.CHANNEL:
            return await temp.edit("<b>❌ ᴏɴʟʏ ᴘᴜʙʟɪᴄ ᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟs ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ.</b>")

        # Check if bot is a member of the channel
        try:
            member = await client.get_chat_member(chat.id, "me")
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await temp.edit(
                    "<b>❌ ʙᴏᴛ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ.</b>\n"
                    "<i>ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴛʜᴇ ʙᴏᴛ ᴀs ᴀɴ ᴀᴅᴍɪɴ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.</i>"
                )
        except UserNotParticipant:
            return await temp.edit(
                "<b>❌ ʙᴏᴛ ɪs ɴᴏᴛ ᴀ ᴍᴇᴍʙᴇʀ ᴏғ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ.</b>\n"
                "<i>ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴍᴀᴋᴇ ɪᴛ ᴀɴ ᴀᴅᴍɪɴ.</i>"
            )

        # Generate invite link
        link = await client.export_chat_invite_link(chat.id) if not chat.username else f"https://t.me/{chat.username}"
        
        # Add channel to database
        await db.add_channel(channel_id)
        return await temp.edit(
            f"<b>✅ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!</b>\n\n"
            f"<b>ɴᴀᴍᴇ:</b> <a href='{link}'>{chat.title}</a>\n"
            f"<b>ɪᴅ:</b> <code>{channel_id}</code>",
            disable_web_page_preview=True
        )

    except PeerIdInvalid:
        return await temp.edit(
            f"<b>❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ:</b>\n<code>{channel_id}</code>\n\n"
            "<i>ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ ɪs ɪɴᴠᴀʟɪᴅ ᴏʀ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ᴅᴏᴇs ɴᴏᴛ ᴇxɪsᴛ. ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ɪᴅ ᴀɴᴅ ᴇɴsᴜʀᴇ ᴛʜᴇ ʙᴏᴛ ɪs ᴀ ᴍᴇᴍʙᴇʀ.</i>"
        )
    except ChatAdminRequired:
        return await temp.edit(
            f"<b>❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ:</b>\n<code>{channel_id}</code>\n\n"
            "<i>ᴛʜᴇ ʙᴏᴛ ʀᴇǫᴜɪʀᴇs ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴀᴄᴄᴇss ᴛʜᴇ ᴄʜᴀɴɴᴇʟ. ᴘʟᴇᴀsᴇ ᴍᴀᴋᴇ ᴛʜᴇ ʙᴏᴛ ᴀɴ ᴀᴅᴍɪɴ.</i>"
        )
    except Exception as e:
        return await temp.edit(
            f"<b>❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ:</b>\n<code>{channel_id}</code>\n\n"
            f"<i>ᴇʀʀᴏʀ: {e}</i>"
        )

@Bot.on_message(filters.command('delchnl') & filters.private & admin)
async def del_force_sub(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    args = message.text.split(maxsplit=1)
    all_channels = await db.show_channels()

    if len(args) < 2:
        buttons = [[InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")]]
        return await temp.edit(
            "<b>ᴜꜱᴀɢᴇ:</b> <code>/delchnl <channel_id | all</code>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    if args[1].lower() == "all":
        if not all_channels:
            return await temp.edit("<b>❌ ɴᴏ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ғᴏᴜɴᴅ.</b>")
        for ch_id in all_channels:
            await db.rem_channel(ch_id)
        return await temp.edit("<b>✅ ᴀʟʟ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ʀᴇᴍᴏᴠᴇᴅ.</b>")

    try:
        ch_id = int(args[1])
        if ch_id in all_channels:
            await db.rem_channel(ch_id)
            return await temp.edit(f"<b>✅ ᴄʜᴀɴɴᴇʟ ʀᴇᴍᴏᴠᴇᴅ:</b> <code>{ch_id}</code>")
        else:
            return await temp.edit(f"<b>❌ ᴄʜᴀɴɴᴇʟ ɴᴏᴛ ғᴏᴜɴᴅ:</b> <code>{ch_id}</code>")
    except ValueError:
        buttons = [[InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")]]
        return await temp.edit(
            "<b>ᴜꜱᴀɢᴇ:</b> <code>/delchnl <channel_id | all</code>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        return await temp.edit(f"<b>❌ ᴇʀʀᴏʀ:</b> <code>{e}</code>")

@Bot.on_message(filters.command('listchnl') & filters.private & admin)
async def list_force_sub_channels(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    channels = await db.show_channels()

    if not channels:
        return await temp.edit("<b>❌ ɴᴏ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ғᴏᴜɴᴅ.</b>")

    result = "<b>⚡ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs:</b>\n\n"
    for ch_id in channels:
        try:
            chat = await client.get_chat(ch_id)
            link = await client.export_chat_invite_link(ch_id) if not chat.username else f"https://t.me/{chat.username}"
            result += f"<b>•</b> <a href='{link}'>{chat.title}</a> [<code>{ch_id}</code>]\n"
        except Exception:
            result += f"<b>•</b> <code>{ch_id}</code> — <i>ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ</i>\n"

    buttons = [[InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")]]
    await temp.edit(
        result, 
        disable_web_page_preview=True, 
        reply_markup=InlineKeyboardMarkup(buttons)
    )

#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#
