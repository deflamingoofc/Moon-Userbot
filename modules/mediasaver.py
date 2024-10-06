import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.me)
async def msave(client: Client, message: Message):
    media = message.reply_to_message.media

    if not media:
        await message.edit("<b>Media is required</b>", parse_mode=enums.ParseMode.HTML)
        return
    await message.delete()

    path = await message.reply_to_message.download()
    # await getattr(client, "send_" + media)("me", path)
    await client.send_document("me", path)
    os.close(path)
    

modules_help["mediasaver"] = {
    "ms": "Save self-destructing media and send it to Saved Messages",
}
