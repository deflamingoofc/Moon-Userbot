import os

from time import perf_counter

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

@Client.on_message(filters.command(["ping"], prefix) & filters.me)
async def ping(_, message: Message):
    start = perf_counter()
    await message.edit("<b>Ping!</b>")
    end = perf_counter()
    await message.edit(f"<b>Pong! {round(end - start, 3)}ms</b>")


modules_help["ping"] = {
    "ping": "periksa ping ke server telegram",
}
