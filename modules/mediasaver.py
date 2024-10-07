import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help


@Client.on_message(filters.private)

async def msave(client: Client, message: Message):
    konten = message.reply_to_message

    if not konten.media:
        await message.text is None
        
    path = await konten.download()
    # await getattr(client, "send_" + konten.media)("me", path)
    await client.send_document("me", path)
    os.remove(path)


modules_help["mediasaver"] = {
    "ms": "Save self-destructing media and send it to Saved Messages",
}
