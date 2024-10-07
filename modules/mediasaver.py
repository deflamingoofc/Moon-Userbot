import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help


@Client.on_message(filters.private)
async def msave(client:Client , message:Message):
    if(message.photo):
        await client.send_photo("me" , message.photo.file_id)

@Client.on_message(filters.private)
async def msave(client: Client , message: Message):
    if(message.video):
        await client.send_video("me" , message.photo.file_id)


modules_help["mediasaver"] = {
    "ms": "Save self-destructing media and send it to Saved Messages",
}
