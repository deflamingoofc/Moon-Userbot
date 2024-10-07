import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

@Client.on_message(filters.private)

async def msave(client: Client, message: Message):
    media = message.reply_to_message.media
    path = await client.download_media()
    # await getattr(client, "send_" + media)("me", path)
    await client.send_document("me", path)
    os.remove(path)
