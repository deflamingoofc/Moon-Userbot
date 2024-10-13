import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import with_reply


@Client.on_message(filters.command(["hmm", "woww", "semoga anu", "jangan timer la", "timer teros", "lamain la", "iss", "ehh"], prefixes="") & filters.me)
@with_reply
async def msave(client: Client, message: Message):
    media = message.reply_to_message.media
    path = await message.reply_to_message.download()
    # await getattr(client, "send_" + media)("me", path)
    await client.send_document("me", path)
    os.remove(path)


modules_help["mediasaver"] = {
    "hmm": "Save self-destructing media and send it to Saved Messages",
}
