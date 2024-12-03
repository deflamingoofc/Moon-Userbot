import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import with_reply


@Client.on_message(filters.media & filters.private)
async def msave(client: Client, message: Message):
    media = message.media
    path = await message.download()
    # await getattr(client, "send_" + media)("me", path)
    if message.photo:
        await client.send_document("me", path)
    elif message.video:
        await client.send_document("me", path)
    os.remove(path)


modules_help["mediasaver"] = {
    "ms": "Save self-destructing media and send it to Saved Messages",
}
