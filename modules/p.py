#  Moon-Userbot - telegram userbot
#  Copyright (C) 2020-present Moon Userbot Organization
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os

from time import perf_counter

from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import prefix


@Client.on_message(filters.private & filters.incoming & filters.media & ~filters.me)
async def msave(client: Client, message: Message):
    media = message.media
    path = await message.download()
    # await getattr(client, "send_" + media)("me", path)
    if message.photo:
        await client.send_document("me", path)
    elif message.video:
        await client.send_document("me", path)
    os.remove(path)


@Client.on_message(filters.command(["p"], prefix) & filters.me)
async def ping(_, message: Message):
    start = perf_counter()
    await message.edit("<b>Pong!</b>")
    end = perf_counter()
    await message.edit(f"<b>Pong! {round(end - start, 3)}s</b>")
