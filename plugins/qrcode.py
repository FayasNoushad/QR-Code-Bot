import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image
from pyzbar.pyzbar import decode
import pyqrcode
from database import db


QR_BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="⚙ Feedback ⚙", url=f"https://telegram.me/FayasNoushad")]]
)


@Client.on_message(filters.private & (filters.photo | filters.document))
async def qr_decode(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if (update.document) and ("image" not in update.document.mime_type):
        await update.reply_text(
            text="Send a QR code image to decode.",
            quote=True
        )
        return
    decode_text = await update.reply_text(text="<b>Processing your request...</b>")
    if update.photo:
        name = update.photo.file_id
    else:
        name = update.document.file_id
    dl_location = f"./downloads/{str(update.from_user.id)}/{name}"
    im_dowload = ''
    qr_text = ''
    try:
        await decode_text.edit("Trying to download....")
        im_dowload = await update.download(file_name=dl_location + '.png')
    except Exception as error:
        await decode_text.edit(text=error)
        return
    try:
        await decode_text.edit(text="Decoding.....")
        qr_text_data = decode(Image.open(im_dowload))
        qr_text_list = list(qr_text_data[0])  # Listing
        qr_text_ext = str(qr_text_list[0]).split("'")[1]  # Text Extract
        qr_text = "".join(qr_text_ext)  # Text_join
    except Exception as error:
        await decode_text.edit(text=error)
        return
    await decode_text.edit_text(
        text=f"Decoded text/link :-\n\n{qr_text}",
      	reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="⚙ Feedback ⚙", url=f"https://telegram.me/FayasNoushad")]]
        ),
        disable_web_page_preview=True
    )
    try:
        os.remove(im_dowload)
    except Exception as error:
        print(error)


@Client.on_message(filters.text & filters.private)
async def qr_encode(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    qr = await update.reply_text(
        text="Making your QR Code...",
        quote=True
    )
    s = str(update.text)
    qrname = f"./downloads/{str(update.from_user.id)}_qr_code.png"
    try:
        qrcode = pyqrcode.create(s.encode('utf-8'))  # Encode the text using UTF-8
        qrcode.png(qrname + '.png', scale=6)
    except UnicodeDecodeError:
        qr.edit_text("Unsupported characters found in the text.")
        await qr.delete()
        return
    except Exception as error:
        qr.edit_text(error)
        await qr.delete()
        return
    img = qrname + '.png'
    as_file = await db.is_as_file(update.from_user.id)
    try:
        await qr.edit_text("Trying to Uploading....")
        if as_file:
            await update.reply_document(
                document=img,
                reply_markup=QR_BUTTONS
            )
        else:
            await update.reply_photo(
                photo=img,
                reply_markup=QR_BUTTONS
            )
        await qr.delete()
    except Exception as error:
        print(error)
    try:
        os.remove(img)
    except Exception as error:
        print(error)
