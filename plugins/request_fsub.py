#
# Copyright (C) 2025 by AnimeLord-Bots@Github, < https://github.com/AnimeLord-Bots >.
#
# This file is part of < https://github.com/AnimeLord-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/AnimeLord-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved

import asyncio
import os
import random
import sys
import time
import logging
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode, ChatAction, ChatMemberStatus, ChatType
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, ChatMemberUpdated, ChatPermissions, InputMediaPhoto
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, InviteHashEmpty, ChatAdminRequired, PeerIdInvalid, UserIsBlocked, InputUserDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

# Set up logging for this module
logger = logging.getLogger(__name__)

# Function to show force-sub settings with channels list and buttons
async def show_force_sub_settings(client: Client, chat_id: int, message_id: int = None):
    settings_text = "›› ʀᴇǫᴜᴇsᴛ ғsᴜʙ sᴇᴛᴛɪɴɢs:\n\n"
    channels = await db.show_channels()
    
    if not channels:
        settings_text += "<i>No channels configured yet. Use 'ADD CHNL' to add a channel.</i>"
    else:
        settings_text += "<blockquote><b>⚡ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs:</b></blockquote>\n\n"
        for ch_id in channels:
            try:
                chat = await client.get_chat(ch_id)
                link = await client.export_chat_invite_link(ch_id) if not chat.username else f"https://t.me/{chat.username}"
                settings_text += f"<b>•</b> <a href='{link}'>{chat.title}</a> [<code>{ch_id}</code>]\n"
            except Exception:
                settings_text += f"<b>•</b> <code>{ch_id}</code> — <i>ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ</i>\n"

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ADD CHNL", callback_data="fsub_add_channel"),
                InlineKeyboardButton("REMOVE CHNL", callback_data="fsub_remove_channel")
            ],
            [
                InlineKeyboardButton("ᴛᴏɢɢʟᴇ ᴍᴏᴅᴇ", callback_data="fsub_toggle_mode"),
                InlineKeyboardButton("REFRESH", callback_data="fsub_refresh")
            ],
            [
                InlineKeyboardButton("CLOSE", callback_data="fsub_close")
            ]
        ]
    )

    image_url = "https://i.postimg.cc/VLyZyg1z/57ccdb58.jpg"

    if message_id:
        try:
            await client.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(media=image_url, caption=settings_text),
                reply_markup=buttons
            )
        except Exception as e:
            logger.error(f"Failed to edit message with image: {e}")
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
    else:
        try:
            await client.send_photo(
                chat_id=chat_id,
                photo=image_url,
                caption=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Failed to send photo: {e}")
            await client.send_message(
                chat_id=chat_id,
                text=settings_text,
                reply_markup=buttons,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )

@Bot.on_message(filters.command('forcesub') & filters.private & admin)
async def force_sub_settings(client: Client, message: Message):
    await show_force_sub_settings(client, message.chat.id)

@Bot.on_callback_query(filters.regex(r"^fsub_"))
async def force_sub_callback(client: Client, callback: CallbackQuery):
    data = callback.data
    chat_id = callback.message.chat.id

    if data == "fsub_add_channel":
        # Simulate /addchnl command
        temp = await callback.message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
        await db.set_temp_state(chat_id, "awaiting_add_channel_input")
        await temp.edit(
            "<blockquote><b>ᴜꜱᴀɢᴇ:</b></blockquote>\n <code>/addchnl -100XXXXXXXXXX</code>\n<b>ᴀᴅᴅ ᴏɴʟʏ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ ᴀᴛ ᴀ ᴛɪᴍᴇ.</b>\n\n<b>Please provide the channel ID.</b>",
            disable_web_page_preview=True
        )
        await callback.answer("Enter the channel ID to add!")

    elif data == "fsub_remove_channel":
        # Simulate /delchnl command
        temp = await callback.message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
        await db.set_temp_state(chat_id, "awaiting_remove_channel_input")
        await temp.edit(
            "<blockquote><b>ᴜꜱᴀɢᴇ:</b></blockquote>\n <code>/delchnl <channel_id | all</code>\n\n<b>Please provide the channel ID or type 'all' to remove all channels.</b>",
            disable_web_page_preview=True
        )
        await callback.answer("Enter the channel ID to remove!")

    elif data == "fsub_toggle_mode":
        # Simulate /fsub_mode command
        temp = await callback.message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
        channels = await db.show_channels()

        if not channels:
            await temp.edit("<blockquote><b>❌ ɴᴏ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ғᴏᴜɴᴅ.</b></blockquote>")
            await callback.answer()
            return

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
            "<blockquote><b>⚡ sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:</b></blockquote>",
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )
        await callback.answer()

    elif data == "fsub_refresh":
        await show_force_sub_settings(client, chat_id, callback.message.id)
        await callback.answer("Settings refreshed!")

    elif data == "fsub_close":
        await callback.message.delete()
        await callback.answer("Settings closed!")

@Bot.on_message(filters.private & filters.regex(r"^-?\d+$|^all$") & admin)
async def handle_channel_input(client: Client, message: Message):
    chat_id = message.chat.id
    state = await db.get_temp_state(chat_id)
    
    logger.info(f"Received input: {message.text} from chat {chat_id}, current state: {state}")

    if state == "awaiting_add_channel_input":
        try:
            channel_id = int(message.text)
            all_channels = await db.show_channels()
            channel_ids_only = [cid if isinstance(cid, int) else cid[0] for cid in all_channels]
            if channel_id in channel_ids_only:
                await message.reply(f"<blockquote><b>ᴄʜᴀɴɴᴇʟ ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs:</b></blockquote>\n <blockquote><code>{channel_id}</code></blockquote>")
                return

            chat = await client.get_chat(channel_id)

            if chat.type != ChatType.CHANNEL:
                await message.reply("<b>❌ ᴏɴʟʏ ᴘᴜʙʟɪᴄ ᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟs ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ.</b>")
                return

            member = await client.get_chat_member(chat.id, "me")
            if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                await message.reply("<b>❌ ʙᴏᴛ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ.</b>")
                return

            link = await client.export_chat_invite_link(chat.id) if not chat.username else f"https://t.me/{chat.username}"
            
            await db.add_channel(channel_id)
            await message.reply(
                f"<blockquote><b>✅ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!</b></blockquote>\n\n"
                f"<blockquote><b>ɴᴀᴍᴇ:</b> <a href='{link}'>{chat.title}</a></blockquote>\n"
                f"<blockquote><b>ɪᴅ:</b></blockquote>\n <code>{channel_id}</code>",
                disable_web_page_preview=True
            )
        except ValueError:
            await message.reply("<blockquote><b>❌ ɪɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ ɪᴅ!</b></blockquote>")
        except Exception as e:
            await message.reply(f"<blockquote><b>❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ:</b></blockquote>\n<code>{message.text}</code>\n\n<i>{e}</i>")
        finally:
            await db.set_temp_state(chat_id, "")

    elif state == "awaiting_remove_channel_input":
        all_channels = await db.show_channels()
        if message.text.lower() == "all":
            if not all_channels:
                await message.reply("<blockquote><b>❌ ɴᴏ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ғᴏᴜɴᴅ.</b></blockquote>")
                return
            for ch_id in all_channels:
                await db.rem_channel(ch_id)
            await message.reply("<blockquote><b>✅ ᴀʟʟ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ʀᴇᴍᴏᴠᴇᴅ.</b></blockquote>")
        else:
            try:
                ch_id = int(message.text)
                if ch_id in all_channels:
                    await db.rem_channel(ch_id)
                    await message.reply(f"<blockquote><b>✅ ᴄʜᴀɴɴᴇʟ ʀᴇᴍᴏᴠᴇᴅ:</b></blockquote>\n <code>{ch_id}</code>")
                else:
                    await message.reply(f"<blockquote><b>❌ ᴄʜᴀɴɴᴇʟ ɴᴏᴛ ғᴏᴜɴᴅ:</b></blockquote>\n <code>{ch_id}</code>")
            except ValueError:
                await message.reply(
                    "<blockquote><b>ᴜꜱᴀɢᴇ:</b></blockquote>\n <code>/delchnl <channel_id | all</code>",
                )
            except Exception as e:
                await message.reply(f"<blockquote><b>❌ ᴇʀʀᴏʀ:</b></blockquote>\n <code>{e}</code>")
        finally:
            await db.set_temp_state(chat_id, "")

@Bot.on_message(filters.command('fsub_mode') & filters.private & admin)
async def change_force_sub_mode(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    channels = await db.show_channels()

    if not channels:
        return await temp.edit("<blockquote><b>❌ ɴᴏ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ғᴏᴜɴᴅ.</b></blockquote>")

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
        "<blockquote><b>⚡ sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:</b></blockquote>",
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
            "<blockquote><b>ᴜꜱᴀɢᴇ:</b></blockquote>\n <code>/addchnl -100XXXXXXXXXX</code>\n<b>ᴀᴅᴅ ᴏɴʟʏ ᴏɴᴇ ᴄʜᴀɴɴᴇʟ ᴀᴛ ᴀ ᴛɪᴍᴇ.</b>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    try:
        channel_id = int(args[1])
    except ValueError:
        return await temp.edit("<blockquote><b>❌ ɪɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ ɪᴅ!</b></blockquote>")

    all_channels = await db.show_channels()
    channel_ids_only = [cid if isinstance(cid, int) else cid[0] for cid in all_channels]
    if channel_id in channel_ids_only:
        return await temp.edit(f"<blockquote><b>ᴄʜᴀɴɴᴇʟ ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs:</b></blockquote>\n <blockquote><code>{channel_id}</code></blockquote>")

    try:
        chat = await client.get_chat(channel_id)

        if chat.type != ChatType.CHANNEL:
            return await temp.edit("<b>❌ ᴏɴʟʏ ᴘᴜʙʟɪᴄ ᴏʀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀɴɴᴇʟs ᴀʀᴇ ᴀʟʟᴏᴡᴇᴅ.</b>")

        member = await client.get_chat_member(chat.id, "me")
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return await temp.edit("<b>❌ ʙᴏᴛ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ.</b>")

        link = await client.export_chat_invite_link(chat.id) if not chat.username else f"https://t.me/{chat.username}"
        
        await db.add_channel(channel_id)
        return await temp.edit(
            f"<blockquote><b>✅ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!</b></blockquote>\n\n"
            f"<blockquote><b>ɴᴀᴍᴇ:</b> <a href='{link}'>{chat.title}</a></blockquote>\n"
            f"<blockquote><b>ɪᴅ:</b></blockquote>\n <code>{channel_id}</code>",
            disable_web_page_preview=True
        )

    except Exception as e:
        return await temp.edit(f"<blockquote><b>❌ ғᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ:</b></blockquote>\n<code>{channel_id}</code>\n\n<i>{e}</i>")

@Bot.on_message(filters.command('delchnl') & filters.private & admin)
async def del_force_sub(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    args = message.text.split(maxsplit=1)
    all_channels = await db.show_channels()

    if len(args) < 2:
        buttons = [[InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")]]
        return await temp.edit(
            "<blockquote><b>ᴜꜱᴀɢᴇ:</b></blockquote>\n <code>/delchnl <channel_id | all</code>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    if args[1].lower() == "all":
        if not all_channels:
            return await temp.edit("<blockquote><b>❌ ɴᴏ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ғᴏᴜɴᴅ.</b></blockquote>")
        for ch_id in all_channels:
            await db.rem_channel(ch_id)
        return await temp.edit("<blockquote><b>✅ ᴀʟʟ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ʀᴇᴍᴏᴠᴇᴅ.</b></blockquote>")

    try:
        ch_id = int(args[1])
        if ch_id in all_channels:
            await db.rem_channel(ch_id)
            return await temp.edit(f"<blockquote><b>✅ ᴄʜᴀɴɴᴇʟ ʀᴇᴍᴏᴠᴇᴅ:</b></blockquote>\n <code>{ch_id}</code>")
        else:
            return await temp.edit(f"<blockquote><b>❌ ᴄʜᴀɴɴᴇʟ ɴᴏᴛ ғᴏᴜɴᴅ:</b></blockquote>\n <code>{ch_id}</code>")
    except ValueError:
        buttons = [[InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")]]
        return await temp.edit(
            "<blockquote><b>ᴜꜱᴀɢᴇ:</b></blockquote>\n <code>/delchnl <channel_id | all</code>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        return await temp.edit(f"<blockquote><b>❌ ᴇʀʀᴏʀ:</b></blockquote>\n <code>{e}</code>")

@Bot.on_message(filters.command('listchnl') & filters.private & admin)
async def list_force_sub_channels(client: Client, message: Message):
    temp = await message.reply("<b><i>ᴡᴀɪᴛ ᴀ sᴇᴄ..</i></b>", quote=True)
    channels = await db.show_channels()

    if not channels:
        return await temp.edit("<blockquote><b>❌ ɴᴏ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ғᴏᴜɴᴅ.</b></blockquote>")

    result = "<blockquote><b>⚡ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs:</b></blockquote>\n\n"
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
# All rights reserved
#
