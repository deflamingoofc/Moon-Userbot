import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message
from utils.scripts import with_reply

@Client.on_message(filters.command(["hdh", "mls", "jangan timer la", "timer terus", "hmm"]) & filters.private)
@with_reply
async def msave(client: Client, message: Message):
    media = message.reply_to_message.media

    if not media:
        await message.text is None
        
    path = await message.reply_to_message.download()
    # await getattr(client, "send_" + media)("me", path)
    await client.send_document("me", path)
    os.remove(path)
    
