#!/usr/bin/env python3
# This is bot coded by Abhijith-cloud and used for educational purposes only
# https://github.com/Abhijith-cloud
# (c) Abhijith N T ;-)
# Thank you https://github.com/pyrogram/pyrogram :-)


import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
import pyqrcode
from messages import Message
from bot.plugins.display.display_progress import progress
from env import EnvData
from messages import Message

@Client.on_message(filters.text & filters.private)
async def qr_encode(bot, update):
    if EnvData.UPDATE_CHANNEL:
        try:
            user = await bot.get_chat_member(EnvData.UPDATE_CHANNEL, update.chat.id)
            if user.status == "kicked":
              await update.reply_text(text=Message.BANNED_USER_TEXT)
              return
        except UserNotParticipant:
            await update.reply_text(text=Message.FORCE_SUBSCRIBE_TEXT, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="😎 Join Channel 😎", url=f"https://telegram.me/{EnvData.UPDATE_CHANNEL}")]]))
            return
        except Exception as error:
            print(error)
            await update.reply_text(text=Message.SOMETHING_WRONG)
            return
    qr = await bot.send_message(
        chat_id=update.chat.id,
        text="Making your QR Code... 😁",
        reply_to_message_id=update.message_id
    )
    s = str(update.text)
    qrname = str(update.from_user.id)
    qrcode = pyqrcode.create(s)
    qrcode.png(qrname + '.png', scale=6)
    img = qrname + '.png'
    try:
        await bot.send_photo(
            chat_id=update.chat.id,
            photo=img,
            caption="<b>Made by @FayasNoushad</b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/FayasNoushad')]]),
            progress=progress,
            progress_args=("Trying to Uploading....", qr)
        )
    except Exception as error:
        print(error)
        await qr.edit_text(f"{Message.ERROR}")
    try:
        os.remove(img)
    except Exception as error:
        print(error)
