# Credits: @mrismanaziz
# Copyright (C) 2022 Pyro-ManUserbot
#
# This file is a part of < https://github.com/mrismanaziz/PyroMan-Userbot/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/mrismanaziz/PyroMan-Userbot/blob/main/LICENSE/>.
#
# t.me/SharingUserbot & t.me/Lunatic0de

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from utils.misc import prefix
from utils.scripts import edit_or_reply


@Client.on_message(filters.command(["kick", "k"], prefix) & filters.me)
async def kickdel_cmd(client: Client, message: Message):
    Man = await edit_or_reply(message, "<b>Kicking deleted accounts...</b>")
    # noinspection PyTypeChecker
    values = [
        await message.chat.ban_member(user.user.id, int(time()) + 31)
        for member in await message.chat.get_members()
        if member.user.is_deleted
    ]
    await Man.edit(f"<b>Successfully kicked {len(values)} deleted account(s)</b>")
