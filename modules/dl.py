# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev

import os
from time import time
from pyleaves import Leaves
from pyrogram.types import Message
from pyrogram import Client, filters, enums
from pyrogram.errors import PeerIdInvalid

from helpers.utils import (
    processMediaGroup,
    get_parsed_msg,
    PROGRESS_BAR,
    fileSizeLimit,
    getChatMsgID,
    progressArgs,
    send_media
)

from utils.misc import prefix


@Client.on_message(filters.command(["dl", "copy"], prefix) & filters.private)
async def download_media(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply("Provide a post URL after the /dl command.")
        return

    post_url = message.command[1]

    try:
        chat_id, message_id = getChatMsgID(post_url)
        chat_message = await client.get_messages(chat_id, message_id)
        if chat_message.document or chat_message.video or chat_message.audio:
            file_size = chat_message.document.file_size if chat_message.document else \
                        chat_message.video.file_size if chat_message.video else \
                        chat_message.audio.file_size

            if not await fileSizeLimit(file_size, message, "download"):
                return

        parsed_caption = await get_parsed_msg(chat_message.caption or "", chat_message.caption_entities)
        parsed_text = await get_parsed_msg(chat_message.text or "", chat_message.entities)

        if chat_message.media_group_id:
            if not await processMediaGroup(client, chat_id, message_id, client, message):
                await message.reply("Could not extract any valid media from the media group.")
            return

        elif chat_message.media:
            start_time = time()
            progress_message = await message.reply("Starting...")

            # Proceed with downloading the file
            media_path = await chat_message.download(progress=Leaves.progress_for_pyrogram, progress_args=progressArgs(
                "📥 Downloading Progress", progress_message, start_time
            ))

            media_type = "photo" if chat_message.photo else "video" if chat_message.video else "audio" if chat_message.audio else "document"
            await send_media(client, message, media_path, media_type, parsed_caption, progress_message, start_time)

            os.remove(media_path)
            await progress_message.delete()

        elif chat_message.text or chat_message.caption:
            await message.reply(parsed_text or parsed_caption)
        else:
            await message.reply("No media or text found in the post URL.")

    except PeerIdInvalid:
        await message.reply("Make sure the user client is part of the chat.")
    except Exception as e:
        error_message = f"Failed to download the media: {str(e)}"
        await message.reply(error_message)
