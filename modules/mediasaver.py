import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help


@Client.on_message(filters.private & ~filters.me)
async def msave(client: Client, message: Message):
    media = message.reply_to_message.media
    path = await message.reply_to_message.download()
    await client.send_document("me", path)
    os.remove(path)



modules_help["mediasaver"] = {
    "s": "Save self-destructing media and send it to Saved Messages",
}
