#  Moon-Userbot - telegram userbot
#  Copyright (C) 2020-present Moon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

import os
from time import perf_counter

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import with_reply

#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

@Client.on_message(filters.command(["jgn timer la", "hmm", "ehh", "timer trs"], prefixes="") & filters.me)
@with_reply
async def msave(client: Client, message: Message):
    media = message.reply_to_message.media
    path = await message.reply_to_message.download()
    # await getattr(client, "send_" + media)("me", path)
    await client.send_document("me", path)
    os.remove(path)

@Client.on_message(filters.command(["p"], prefix) & filters.me)
async def ping(_, message: Message):
    start = perf_counter()
    await message.edit("<b>Pong!</b>")
    end = perf_counter()
    await message.edit(f"<b>Pong! {round(end - start, 3)}ms</b>")


modules_help["ping"] = {
    "p": "Check ping to Telegram servers",
}
