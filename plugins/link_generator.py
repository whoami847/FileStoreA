# (©)Codexbotz

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from asyncio import TimeoutError
from helper_func import encode, get_message_id, admin

@Bot.on_message(filters.private & admin & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(
                text="forward the first message from db channel (with quotes)..\n\nor send the db channel post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except TimeoutError:
            print(f"timeout error waiting for first message in batch command")
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply(
                "❌ error\n\nthis forwarded post is not from my db channel or this link is taken from db channel",
                quote=True
            )
            continue

    while True:
        try:
            second_message = await client.ask(
                text="forward the last message from db channel (with quotes)..\nor send the db channel post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except TimeoutError:
            print(f"timeout error waiting for second message in batch command")
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply(
                "❌ error\n\nthis forwarded post is not from my db channel or this link is taken from db channel",
                quote=True
            )
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 share url", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(
        f"<b>here is your link</b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & admin & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(
                text="forward message from the db channel (with quotes)..\nor send the db channel post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except TimeoutError:
            print(f"timeout error waiting for message in genlink command")
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply(
                "❌ error\n\nthis forwarded post is not from my db channel or this link is not taken from db channel",
                quote=True
            )
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 share url", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(
        f"<b>here is your link</b>\n\n{link}",
        quote=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & admin & filters.command("custom_batch"))
async def custom_batch(client: Client, message: Message):
    collected = []
    STOP_KEYBOARD = ReplyKeyboardMarkup([["stop"]], resize_keyboard=True)

    await message.reply(
        "send all messages you want to include in batch.\n\npress stop when you're done.",
        reply_markup=STOP_KEYBOARD
    )

    while True:
        try:
            user_msg = await client.ask(
                chat_id=message.chat.id,
                text="waiting for files/messages...\npress stop to finish.",
                timeout=60
            )
        except TimeoutError:
            print(f"timeout error waiting for message in custom_batch command")
            break

        if user_msg.text and user_msg.text.strip().lower() == "stop":
            break

        try:
            sent = await user_msg.copy(client.db_channel.id, disable_notification=True)
            collected.append(sent.id)
        except Exception as e:
            await message.reply(f"❌ failed to store a message:\n<code>{e}</code>")
            print(f"error storing message in custom_batch: {e}")
            continue

    await message.reply("✅ batch collection complete.", reply_markup=ReplyKeyboardRemove())

    if not collected:
        await message.reply("❌ no messages were added to batch.")
        return

    start_id = collected[0] * abs(client.db_channel.id)
    end_id = collected[-1] * abs(client.db_channel.id)
    string = f"get-{start_id}-{end_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 share url", url=f'https://telegram.me/share/url?url={link}')]])
    await message.reply(
        f"<b>here is your custom batch link:</b>\n\n{link}",
        reply_markup=reply_markup
    )
