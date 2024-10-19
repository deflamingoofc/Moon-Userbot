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

from contextlib import suppress

from pyrogram import Client, ContinuePropagation, filters
from pyrogram.errors import (
    UserAdminInvalid,
    ChatAdminRequired,
    RPCError,
)
from pyrogram.raw import functions
from pyrogram.types import Message, ChatPermissions

from utils.db import db
from utils.scripts import format_exc, with_reply
from utils.misc import modules_help, prefix

from utils.handlers import (
    KickDeletedAccountsHandler,
)


db_cache: dict = db.get_collection("core.ats")


def update_cache():
    db_cache.clear()
    db_cache.update(db.get_collection("core.ats"))


@Client.on_message(filters.group & ~filters.me)
async def admintool_handler(_, message: Message):
    if message.sender_chat and (
        message.sender_chat.type == "supergroup"
        or message.sender_chat.id == db_cache.get(f"linked{message.chat.id}", 0)
    ):
        raise ContinuePropagation

    if message.sender_chat and db_cache.get(f"antich{message.chat.id}", False):
        with suppress(RPCError):
            await message.delete()
            await message.chat.ban_member(message.sender_chat.id)

    tmuted_users = db_cache.get(f"c{message.chat.id}", [])
    if (
        message.from_user
        and message.from_user.id in tmuted_users
        or message.sender_chat
        and message.sender_chat.id in tmuted_users
    ):
        with suppress(RPCError):
            await message.delete()

    if db_cache.get(f"antiraid{message.chat.id}", False):
        with suppress(RPCError):
            await message.delete()
            if message.from_user:
                await message.chat.ban_member(message.from_user.id)
            elif message.sender_chat:
                await message.chat.ban_member(message.sender_chat.id)

    if message.new_chat_members and db_cache.get(
        f"welcome_enabled{message.chat.id}", False
    ):
        await message.reply(
            db_cache.get(f"welcome_text{message.chat.id}"),
            disable_web_page_preview=True,
        )

    raise ContinuePropagation


async def get_user_and_name(message):
    if message.reply_to_message.from_user:
        return (
            message.reply_to_message.from_user.id,
            message.reply_to_message.from_user.first_name,
        )
    if message.reply_to_message.sender_chat:
        return (
            message.reply_to_message.sender_chat.id,
            message.reply_to_message.sender_chat.title,
        )



@Client.on_message(filters.command(["kickdeak"], prefix) & filters.me)
async def kickdel_cmd(client: Client, message: Message):
    handler = KickDeletedAccountsHandler(client, message)
    await handler.kick_deleted_accounts()



modules_help["kickdeak"] = {
    "kickdeak": "Kick all deleted accounts",
}
