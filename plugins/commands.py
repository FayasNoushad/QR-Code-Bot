from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db


START_TEXT = """**Hello {} 😌
I am a QR Code Bot**

>> `I can generate links to QR Code with QR Code decode to links support.`

Made by @FayasNoushad"""

HELP_TEXT = """**Hey, Follow these steps:**

➠ Send me a link I will generate the QR code of that link
➠ Send me a QR code image I will decode that image and convert to link

**Available Commands**

/start - Checking Bot Online
/help - For more help
/about - For more about me
/settings - For bot settings
/reset - For reset settings
/status - For bot status

Made by @FayasNoushad"""

ABOUT_TEXT = """--**About Me 😎**--

🤖 **Name :** [QR Code Bot](https://telegram.me/{})

👨‍💻 **Developer :** [Fayas](https://github.com/FayasNoushad)

📢 **Channel :** [Fayas Noushad](https://telegram.me/FayasNoushad)

👥 **Group :** [Developer Team](https://telegram.me/TheDeveloperTeam)

🌐 **Source :** [👉 Click here](https://github.com/AbhijithNT/QRCode-Telegram-bot)

📝 **Language :** [Python3](https://python.org)

🧰 **Framework :** [Pyrogram](https://pyrogram.org)

📡 **Server :** [Heroku](https://heroku.com)"""

SETTINGS_TEXT = "**Settings**"

FORCE_SUBSCRIBE_TEXT = "<code>Sorry Dear You Must Join My Updates Channel for using me 😌😉....</code>"

START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('⚙ Help', callback_data='help'),
        InlineKeyboardButton('About 🔰', callback_data='about'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )

HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('About 🔰', callback_data='about')
        ],[
        InlineKeyboardButton('⚒ Settings', callback_data='settings'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )

ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏘 Home', callback_data='home'),
        InlineKeyboardButton('Help ⚙', callback_data='help'),
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]]
    )


@Client.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "lol":
        await update.answer(
            text="Select a button below",
            show_alert=True
        )
    elif update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "settings":
        await display_settings(bot, update, db, cb=True, cb_text=True)
    elif update.data == "close":
        await update.message.delete()
    elif update.data == "set_af":
        as_file = await db.is_as_file(update.from_user.id)
        await db.update_as_file(update.from_user.id, not as_file)
        if as_file:
            alert_text = "Upload mode changed to file successfully"
        else:
            alert_text = "Upload mode changed to photo successfully"
        await update.answer(text=alert_text, show_alert=True)
        await display_settings(bot, update, db, cb=True)


@Client.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
      	reply_markup=START_BUTTONS,
      	quote=True
    )


@Client.on_message(filters.private & filters.command(["help"]))
async def help(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=HELP_TEXT,
      	disable_web_page_preview=True,
      	reply_markup=HELP_BUTTONS,
      	quote=True
    )


@Client.on_message(filters.private & filters.command(["about"]))
async def about(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await update.reply_text(
        text=ABOUT_TEXT,
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS,
        quote=True
    )


@Client.on_message(filters.private & filters.command(["reset"]))
async def reset(bot, update):
    await db.delete_user(update.from_user.id)
    await db.add_user(update.from_user.id)
    await update.reply_text("Settings reset successfully")


@Client.on_message(filters.private & filters.command(["settings"]))
async def settings(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    await display_settings(bot, update, db)


async def display_settings(bot, update, db, cb=False, cb_text=False):
    chat_id = update.from_user.id
    as_file = await db.is_as_file(chat_id)
    as_file_btn = [
        InlineKeyboardButton("Upload Mode", callback_data="lol")
    ]
    if as_file:
        as_file_btn.append(
            InlineKeyboardButton('Upload as File', callback_data='set_af')
        )
    else:
        as_file_btn.append(
            InlineKeyboardButton('Upload as Photo', callback_data='set_af')
        )
    close_btn = [
        InlineKeyboardButton('Close ✖️', callback_data='close')
        ]
    settings_buttons = [as_file_btn, close_btn]
    try:
        if cb:
            if cb and cb_text:
                await update.message.edit_text(
                    text=SETTINGS_TEXT,
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(settings_buttons)
                )
            else:
                await update.edit_message_reply_markup(
                    InlineKeyboardMarkup(settings_buttons)
                )
        else:
            await update.reply_text(
                text=SETTINGS_TEXT,
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(settings_buttons)
            )
    except Exception as error:
        print(error)


@Client.on_message(filters.private & filters.command("status"))
async def status(bot, update):
    total_users = await db.total_users_count()
    text = "**Bot Status**\n"
    text += f"\n**Total Users:** `{total_users}`"
    await update.reply_text(
        text=text,
        quote=True,
        disable_web_page_preview=True
    )
