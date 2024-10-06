import os

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help


@Client.on_message(filters.private | filters.photo)
async def saveImage(client:Client , message:Message):
    if(message.photo.ttl_seconds):
        await client.send_photo("me" , message.photo.file_id)

@Client.on_message(filters.private | filters.photo)
async def saveVideo(client:Client , message:Message):
    if(message.video.ttl_seconds):
        await client.send_video("me" , message.photo.file_id)
    


modules_help["mediasaver"] = {
    "mediasaver": "Automatically save self-destructing media and send it to Saved Messages",
}
