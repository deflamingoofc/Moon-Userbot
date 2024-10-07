import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help

@Client.on_message(filters.private)

async def msave(client: Client, message: Message):
    kosong = message.text is None
    if not message.reply_to_message.media:
        await message.edit("kosong")
    path = await message.reply_to_message.download()
    # await getattr(client, "send_" + message.reply_to_message.media)("me", path)
    await client.send_document("me", path)
    os.remove(path)


modules_help["mediasaver"] = {
    "ms": "Save self-destructing media and send it to Saved Messages",
}
