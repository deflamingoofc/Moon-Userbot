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

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import format_exc, interact_with, interact_with_to_delete


@Client.on_message(filters.command("id", prefix) & filters.me)
async def get_user_inf(client: Client, message: Message):
    if len(message.command) >= 2:
        peer = await client.resolve_peer(message.command[1])
    elif message.reply_to_message and message.reply_to_message.from_user:
        peer = await client.resolve_peer(message.reply_to_message.from_user.id)
    else:
        peer = await client.resolve_peer("me")

    response = await client.invoke(functions.users.GetFullUser(id=peer))

    user = response.users[0]
    full_user = response.full_user

    if user.username is None:
        username = "None"
    else:
        username = f"@{user.username}"
    about = "None" if full_user.about is None else full_user.about

    user_info = f"""ユーザーID <b><code>{user.first_name}</code></b> は : <code>{user.id}</code>
"""
    await message.edit(user_info)


modules_help["id"] = {
    "id [reply|id|username]": "melihat id pengguna",
}
