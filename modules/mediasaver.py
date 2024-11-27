import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help


@Client.on_message(filters.me)
async def msave(client: Client, message: Message):
  media = message.media.value
  path = await message.download_media()
  # await getattr(client, "send_" + media)("me", path)
  await client.send_document("me", path)
  os.remove(path)


modules_help["mediasaver"] = {
    "ms": "Save self-destructing media and send it to Saved Messages",
}
