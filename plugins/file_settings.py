import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PROTECT_CONTENT, HIDE_CAPTION, DISABLE_CHANNEL_BUTTON, BUTTON_NAME, BUTTON_LINK
from database.database import Database

db = Database()
logger = logging.getLogger(__name__)

async def refresh_settings():
    global PROTECT_CONTENT, HIDE_CAPTION, DISABLE_CHANNEL_BUTTON, BUTTON_NAME, BUTTON_LINK
    settings = await db.get_settings()
    PROTECT_CONTENT = settings.get('PROTECT_CONTENT', False)
    HIDE_CAPTION = settings.get('HIDE_CAPTION', False)
    DISABLE_CHANNEL_BUTTON = settings.get('DISABLE_CHANNEL_BUTTON', True)
    BUTTON_NAME = settings.get('BUTTON_NAME', None)
    BUTTON_LINK = settings.get('BUTTON_LINK', None)
    logger.info(f"Settings refreshed: PROTECT_CONTENT={PROTECT_CONTENT}, HIDE_CAPTION={HIDE_CAPTION}, DISABLE_CHANNEL_BUTTON={DISABLE_CHANNEL_BUTTON}")

async def show_settings_message(client, callback_query, is_callback=False):
    settings = await db.get_settings()
    protect_content = settings.get('PROTECT_CONTENT', False)
    hide_caption = settings.get('HIDE_CAPTION', False)
    disable_channel_button = settings.get('DISABLE_CHANNEL_BUTTON', True)
    button_name = settings.get('BUTTON_NAME', "Not Set")
    button_link = settings.get('BUTTON_LINK', "Not Set")

    text = (
        "⚙️ **Bot Settings**\n\n"
        f"**Protect Content**: {'✅ Enabled' if protect_content else '❌ Disabled'}\n"
        f"**Hide Caption**: {'✅ Enabled' if hide_caption else '❌ Disabled'}\n"
        f"**Disable Channel Button**: {'✅ Enabled' if disable_channel_button else '❌ Disabled'}\n"
        f"**Button Name**: {button_name}\n"
        f"**Button Link**: {button_link}"
    )

    buttons = [
        [
            InlineKeyboardButton("Protect Content", callback_data="toggle_protect_content"),
            InlineKeyboardButton("Hide Caption", callback_data="toggle_hide_caption")
        ],
        [
            InlineKeyboardButton("Disable Channel Button", callback_data="toggle_channel_button"),
            InlineKeyboardButton("Set Button", callback_data="set_btn")  # Changed to set_btn
        ],
        [InlineKeyboardButton("Refresh", callback_data="refresh_settings")],
        [InlineKeyboardButton("Close", callback_data="close")]
    ]

    if is_callback:
        await callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await callback_query.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.command("fsettings") & filters.private & filters.user(ADMINS))
async def fsettings_command(client, message):
    await show_settings_message(client, message)

@Client.on_callback_query(filters.regex("toggle_protect_content"))
async def toggle_protect_content(client, callback_query):
    settings = await db.get_settings()
    new_value = not settings.get('PROTECT_CONTENT', False)
    await db.update_setting('PROTECT_CONTENT', new_value)
    await refresh_settings()
    await show_settings_message(client, callback_query, is_callback=True)
    await callback_query.answer(f"Protect Content {'enabled' if new_value else 'disabled'}!")

@Client.on_callback_query(filters.regex("toggle_hide_caption"))
async def toggle_hide_caption(client, callback_query):
    settings = await db.get_settings()
    new_value = not settings.get('HIDE_CAPTION', False)
    await db.update_setting('HIDE_CAPTION', new_value)
    await refresh_settings()
    await show_settings_message(client, callback_query, is_callback=True)
    await callback_query.answer(f"Hide Caption {'enabled' if new_value else 'disabled'}!")

@Client.on_callback_query(filters.regex("toggle_channel_button"))
async def toggle_channel_button(client, callback_query):
    settings = await db.get_settings()
    new_value = not settings.get('DISABLE_CHANNEL_BUTTON', True)
    await db.update_setting('DISABLE_CHANNEL_BUTTON', new_value)
    await refresh_settings()
    await show_settings_message(client, callback_query, is_callback=True)
    await callback_query.answer(f"Disable Channel Button {'enabled' if new_value else 'disabled'}!")

@Client.on_callback_query(filters.regex("refresh_settings"))
async def refresh_settings_message(client, callback_query):
    await refresh_settings()
    await show_settings_message(client, callback_query, is_callback=True)
    await callback_query.answer("Settings refreshed!")

@Client.on_callback_query(filters.regex("set_btn"))
async def set_button_start(client, callback_query):
    logger.info(f"set_btn callback triggered by user {callback_query.from_user.id}")
    await callback_query.message.reply_text("Please enter the new Button Name:")
    await callback_query.answer()
    client.add_handler(MessageHandler(set_button_name, filters.private & filters.user(callback_query.from_user.id)), group=1)

async def set_button_name(client, message):
    button_name = message.text.strip()
    if not button_name:
        await message.reply_text("Button name cannot be empty. Please try again:")
        return
    await db.update_setting('BUTTON_NAME', button_name)
    await refresh_settings()
    await message.reply_text("Button name saved! Now, please enter the Button Link:")
    client.add_handler(MessageHandler(set_button_link, filters.private & filters.user(message.from_user.id)), group=1)

async def set_button_link(client, message):
    button_link = message.text.strip()
    if not button_link:
        await message.reply_text("Button link cannot be empty. Please try again:")
        return
    await db.update_setting('BUTTON_LINK', button_link)
    await refresh_settings()
    await message.reply_text("Button link saved!")
    client.remove_handler(MessageHandler(set_button_name, filters.private & filters.user(message.from_user.id)), group=1)
    client.remove_handler(MessageHandler(set_button_link, filters.private & filters.user(message.from_user.id)), group=1)
