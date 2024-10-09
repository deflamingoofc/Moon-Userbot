import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

@Client.on_message(filters.command(["hdhh", "unch", "jangan timer la", "timer terus", "hmm", "anu kah", "semoga anu"], prefixes="") & filters.private)

async def msave(client: Client, message: Message):
    media = message.reply_to_message.media

    if not media:
        await message.text()
        return
    await message.delete()

    path = await message.reply_to_message.download()
    # await getattr(client, "send_" + media)("me", path)
    await client.send_document("me", path)
    os.remove(path)
