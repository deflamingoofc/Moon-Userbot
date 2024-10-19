import asyncio
import os
from contextlib import suppress
from subprocess import PIPE

import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc, import_library, with_reply, restart

import_library("pytgcalls", "pytgcalls==3.0.0.dev24")
import_library("yt_dlp")

from pytgcalls import GroupCallFactory

GROUP_CALL = None


def init_client(func):
    async def wrapper(client, message):
        global GROUP_CALL
        if not GROUP_CALL:
            GROUP_CALL = GroupCallFactory(client).get_file_group_call()
            GROUP_CALL.enable_logs_to_console = False

        return await func(client, message)

    return wrapper



@Client.on_message(filters.command("join", prefix) & filters.me)
@init_client
async def start(_, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    with suppress(ValueError):
        chat_id = int(chat_id)

    try:
        await GROUP_CALL.start(chat_id)
        await message.edit("<b>Joined VC successfully!</b>")
    except Exception as e:
        await message.edit(f"<b>An unexpected error has occurred: <code>{e}</code></b>")


@Client.on_message(filters.command("leave_vc", prefix) & filters.me)
@init_client
async def stop(_, message: Message):
    try:
        if os.path.exists("input.raw"):
            os.remove("input.raw")
        await GROUP_CALL.stop()
        await message.edit("<b>Leaving successfully!</b>")
    except Exception as e:
        await message.edit(
            f"<b>Аn unexpected error occurred [<code>{e}</code>]\n"
            "The bot will try to exit the voice chat by restarting itself,"
            "the bot will be unavailable for the next 4 seconds</b>"
        )
        restart()



modules_help["voice_chat"] = {
    "join [chat_id]": "Join the voice chat",
    "leave_vc": "Leave voice chat",
}
