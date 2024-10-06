import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help


@Client.on_message(filters.private | filters.photo)
async def msave(client:Client , message:Message):
    if(message.photo.media):
        await client.send_photo("me" , message.photo.file_id)

@Client.on_message(filters.private | filters.photo)
async def msave(client:Client , message:Message):
    if(message.video.media):
        await client.send_video("me" , message.video.file_id)
    


modules_help["mediasaver"] = {
    "mediasaver": "Automatically save self-destructing media and send it to Saved Messages",
}
