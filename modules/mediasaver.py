import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

@Client.on_message(filters.private | filters.media)

async def msave(client: Client, message: Message):
    if(message.reply_to_message.media)
    path = await message.reply_to_message.download()
    # await getattr(client, "send_" + media)("me", path)
    await client.send_document("me", path)
    os.remove(path)
