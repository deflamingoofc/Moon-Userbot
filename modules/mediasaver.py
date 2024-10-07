import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help


@Client.on_message(filters.private & filters.incoming & ~filters.service & ~filters.me)
async def media_filter(video, photo, m: Message):
    return bool(m.media)
    path = await message.download()
    await client.send_document("me", path)
    os.remove(path)


modules_help["mediasaver"] = {
    "s": "Save self-destructing media and send it to Saved Messages",
}
