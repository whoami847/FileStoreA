from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import PROTECT_CONTENT, HIDE_CAPTION, DISABLE_CHANNEL_BUTTON, BUTTON_NAME, BUTTON_LINK, update_setting, get_settings
from database.database import db

@Client.on_message(filters.command("fsettings") & filters.private)
async def fsettings(client, message):
    settings = get_settings()
    text = (
        "⚙️ **File Settings**\n\n"
        f"**Protect Content:** {'✅ Enabled' if settings['PROTECT_CONTENT'] else '❌ Disabled'}\n"
        f"**Hide Caption:** {'✅ Enabled' if settings['HIDE_CAPTION'] else '❌ Disabled'}\n"
        f"**Channel Button:** {'✅ Enabled' if not settings['DISABLE_CHANNEL_BUTTON'] else '❌ Disabled'}\n"
        f"**Custom Button:** {settings['BUTTON_NAME'] if settings['BUTTON_NAME'] else 'Not Set'} ({settings['BUTTON_LINK'] if settings['BUTTON_LINK'] else 'No Link'})"
    )

    buttons = [
        [
            InlineKeyboardButton("PC", callback_data="toggle_pc"),
            InlineKeyboardButton("HC", callback_data="toggle_hc"),
            InlineKeyboardButton("CB", callback_data="toggle_cb")
        ],
        [InlineKeyboardButton("SB", callback_data="custom_set_button")],
        [
            InlineKeyboardButton("Refresh", callback_data="refresh_settings"),
            InlineKeyboardButton("Back", callback_data="back_to_start")
        ]
    ]

    await message.reply(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True
    )

@Client.on_callback_query(filters.regex(r"toggle_pc"))
async def toggle_protect_content(client, callback_query):
    settings = get_settings()
    new_value = not settings["PROTECT_CONTENT"]
    await update_setting("PROTECT_CONTENT", new_value)
    
    updated_settings = get_settings()
    text = (
        "⚙️ **File Settings**\n\n"
        f"**Protect Content:** {'✅ Enabled' if updated_settings['PROTECT_CONTENT'] else '❌ Disabled'}\n"
        f"**Hide Caption:** {'✅ Enabled' if updated_settings['HIDE_CAPTION'] else '❌ Disabled'}\n"
        f"**Channel Button:** {'✅ Enabled' if not updated_settings['DISABLE_CHANNEL_BUTTON'] else '❌ Disabled'}\n"
        f"**Custom Button:** {updated_settings['BUTTON_NAME'] if updated_settings['BUTTON_NAME'] else 'Not Set'} ({updated_settings['BUTTON_LINK'] if updated_settings['BUTTON_LINK'] else 'No Link'})"
    )

    buttons = [
        [
            InlineKeyboardButton("PC", callback_data="toggle_pc"),
            InlineKeyboardButton("HC", callback_data="toggle_hc"),
            InlineKeyboardButton("CB", callback_data="toggle_cb")
        ],
        [InlineKeyboardButton("SB", callback_data="custom_set_button")],
        [
            InlineKeyboardButton("Refresh", callback_data="refresh_settings"),
            InlineKeyboardButton("Back", callback_data="back_to_start")
        ]
    ]

    await callback_query.message.edit(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer("Protect Content setting updated!")

@Client.on_callback_query(filters.regex(r"toggle_hc"))
async def toggle_hide_caption(client, callback_query):
    settings = get_settings()
    new_value = not settings["HIDE_CAPTION"]
    await update_setting("HIDE_CAPTION", new_value)
    
    updated_settings = get_settings()
    text = (
        "⚙️ **File Settings**\n\n"
        f"**Protect Content:** {'✅ Enabled' if updated_settings['PROTECT_CONTENT'] else '❌ Disabled'}\n"
        f"**Hide Caption:** {'✅ Enabled' if updated_settings['HIDE_CAPTION'] else '❌ Disabled'}\n"
        f"**Channel Button:** {'✅ Enabled' if not updated_settings['DISABLE_CHANNEL_BUTTON'] else '❌ Disabled'}\n"
        f"**Custom Button:** {updated_settings['BUTTON_NAME'] if updated_settings['BUTTON_NAME'] else 'Not Set'} ({updated_settings['BUTTON_LINK'] if updated_settings['BUTTON_LINK'] else 'No Link'})"
    )

    buttons = [
        [
            InlineKeyboardButton("PC", callback_data="toggle_pc"),
            InlineKeyboardButton("HC", callback_data="toggle_hc"),
            InlineKeyboardButton("CB", callback_data="toggle_cb")
        ],
        [InlineKeyboardButton("SB", callback_data="custom_set_button")],
        [
            InlineKeyboardButton("Refresh", callback_data="refresh_settings"),
            InlineKeyboardButton("Back", callback_data="back_to_start")
        ]
    ]

    await callback_query.message.edit(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer("Hide Caption setting updated!")

@Client.on_callback_query(filters.regex(r"toggle_cb"))
async def toggle_channel_button(client, callback_query):
    settings = get_settings()
    new_value = not settings["DISABLE_CHANNEL_BUTTON"]
    await update_setting("DISABLE_CHANNEL_BUTTON", new_value)
    
    updated_settings = get_settings()
    text = (
        "⚙️ **File Settings**\n\n"
        f"**Protect Content:** {'✅ Enabled' if updated_settings['PROTECT_CONTENT'] else '❌ Disabled'}\n"
        f"**Hide Caption:** {'✅ Enabled' if updated_settings['HIDE_CAPTION'] else '❌ Disabled'}\n"
        f"**Channel Button:** {'✅ Enabled' if not updated_settings['DISABLE_CHANNEL_BUTTON'] else '❌ Disabled'}\n"
        f"**Custom Button:** {updated_settings['BUTTON_NAME'] if updated_settings['BUTTON_NAME'] else 'Not Set'} ({updated_settings['BUTTON_LINK'] if updated_settings['BUTTON_LINK'] else 'No Link'})"
    )

    buttons = [
        [
            InlineKeyboardButton("PC", callback_data="toggle_pc"),
            InlineKeyboardButton("HC", callback_data="toggle_hc"),
            InlineKeyboardButton("CB", callback_data="toggle_cb")
        ],
        [InlineKeyboardButton("SB", callback_data="custom_set_button")],
        [
            InlineKeyboardButton("Refresh", callback_data="refresh_settings"),
            InlineKeyboardButton("Back", callback_data="back_to_start")
        ]
    ]

    await callback_query.message.edit(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer("Channel Button setting updated!")

@Client.on_callback_query(filters.regex(r"custom_set_button"))
async def set_button(client, callback_query):
    await db.set_temp_state(callback_query.from_user.id, "awaiting_button_name")
    await callback_query.message.edit(
        text="Please send the button name (e.g., 'Join Channel'):",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Cancel", callback_data="cancel_set_button")]
        ])
    )
    await callback_query.answer()

@Client.on_message(filters.text & filters.private)
async def handle_button_input(client, message):
    user_id = message.from_user.id
    state = await db.get_temp_state(user_id)

    if state == "awaiting_button_name":
        button_name = message.text
        await db.set_temp_state(user_id, f"awaiting_button_link_{button_name}")
        await message.reply(
            text=f"Button name set to: {button_name}\nNow, please send the button link (e.g., 'https://t.me/yourchannel'):",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Cancel", callback_data="cancel_set_button")]
            ])
        )
    elif state.startswith("awaiting_button_link_"):
        button_name = state.split("awaiting_button_link_")[1]
        button_link = message.text

        # Update the button settings
        await update_setting("BUTTON_NAME", button_name)
        await update_setting("BUTTON_LINK", button_link)

        # Clear the temp state
        await db.set_temp_state(user_id, "")

        # Update the settings message
        settings = get_settings()
        text = (
            "⚙️ **File Settings**\n\n"
            f"**Protect Content:** {'✅ Enabled' if settings['PROTECT_CONTENT'] else '❌ Disabled'}\n"
            f"**Hide Caption:** {'✅ Enabled' if settings['HIDE_CAPTION'] else '❌ Disabled'}\n"
            f"**Channel Button:** {'✅ Enabled' if not settings['DISABLE_CHANNEL_BUTTON'] else '❌ Disabled'}\n"
            f"**Custom Button:** {settings['BUTTON_NAME'] if settings['BUTTON_NAME'] else 'Not Set'} ({settings['BUTTON_LINK'] if settings['BUTTON_LINK'] else 'No Link'})"
        )

        buttons = [
            [
                InlineKeyboardButton("PC", callback_data="toggle_pc"),
                InlineKeyboardButton("HC", callback_data="toggle_hc"),
                InlineKeyboardButton("CB", callback_data="toggle_cb")
            ],
        [InlineKeyboardButton("SB", callback_data="custom_set_button")],
            [
                InlineKeyboardButton("Refresh", callback_data="refresh_settings"),
                InlineKeyboardButton("Back", callback_data="back_to_start")
            ]
        ]

        await message.reply(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

@Client.on_callback_query(filters.regex(r"cancel_set_button"))
async def cancel_set_button(client, callback_query):
    await db.set_temp_state(callback_query.from_user.id, "")
    settings = get_settings()
    text = (
        "⚙️ **File Settings**\n\n"
        f"**Protect Content:** {'✅ Enabled' if settings['PROTECT_CONTENT'] else '❌ Disabled'}\n"
        f"**Hide Caption:** {'✅ Enabled' if settings['HIDE_CAPTION'] else '❌ Disabled'}\n"
        f"**Channel Button:** {'✅ Enabled' if not settings['DISABLE_CHANNEL_BUTTON'] else '❌ Disabled'}\n"
        f"**Custom Button:** {settings['BUTTON_NAME'] if settings['BUTTON_NAME'] else 'Not Set'} ({settings['BUTTON_LINK'] if settings['BUTTON_LINK'] else 'No Link'})"
    )

    buttons = [
        [
            InlineKeyboardButton("PC", callback_data="toggle_pc"),
            InlineKeyboardButton("HC", callback_data="toggle_hc"),
            InlineKeyboardButton("CB", callback_data="toggle_cb")
        ],
        [InlineKeyboardButton("SB", callback_data="custom_set_button")],
        [
            InlineKeyboardButton("Refresh", callback_data="refresh_settings"),
            InlineKeyboardButton("Back", callback_data="back_to_start")
        ]
    ]

    await callback_query.message.edit(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer("Cancelled button setting.")

@Client.on_callback_query(filters.regex(r"refresh_settings"))
async def refresh_settings(client, callback_query):
    settings = get_settings()
    text = (
        "⚙️ **File Settings**\n\n"
        f"**Protect Content:** {'✅ Enabled' if settings['PROTECT_CONTENT'] else '❌ Disabled'}\n"
        f"**Hide Caption:** {'✅ Enabled' if settings['HIDE_CAPTION'] else '❌ Disabled'}\n"
        f"**Channel Button:** {'✅ Enabled' if not settings['DISABLE_CHANNEL_BUTTON'] else '❌ Disabled'}\n"
        f"**Custom Button:** {settings['BUTTON_NAME'] if settings['BUTTON_NAME'] else 'Not Set'} ({settings['BUTTON_LINK'] if settings['BUTTON_LINK'] else 'No Link'})"
    )

    buttons = [
        [
            InlineKeyboardButton("PC", callback_data="toggle_pc"),
            InlineKeyboardButton("HC", callback_data="toggle_hc"),
            InlineKeyboardButton("CB", callback_data="toggle_cb")
        ],
        [InlineKeyboardButton("SB", callback_data="custom_set_button")],
        [
            InlineKeyboardButton("Refresh", callback_data="refresh_settings"),
            InlineKeyboardButton("Back", callback_data="back_to_start")
        ]
    ]

    await callback_query.message.edit(
        text=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer("Settings refreshed!")

@Client.on_callback_query(filters.regex(r"back_to_start"))
async def back_to_start(client, callback_query):
    await callback_query.message.delete()
    await callback_query.message.reply("Back to start! Use /start to begin again.")
    await callback_query.answer()
