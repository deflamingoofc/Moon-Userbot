import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help
from utils.scripts import save_media

@Client.on_message(filters.private)
@save_media
async def msave(client: Client, message: Message):
    media = message.reply_to_message.media
    kosong = message.empty
    if not media:
        await message.edit("kosong")
        
    path = await message.reply_to_message.download()
    # await getattr(client, "send_" + media)("me", path)
    await client.send_document("me", path)
    os.remove(path)


modules_help["mediasaver"] = {
    "ms": "Save self-destructing media and send it to Saved Messages",
}
