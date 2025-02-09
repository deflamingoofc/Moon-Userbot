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


from datetime import datetime, timedelta

from pyrogram import Client
from pyrogram.types import Message


class KickDeletedAccountsHandler:
    def __init__(self, client: Client, message: Message):
        self.client = client
        self.message = message
        self.chat_id = message.chat.id
        self.kicked_count = 0

    async def kick_deleted_accounts(self):
        await self.message.edit("<b>Kicking deleted accounts...</b>")
        try:
            async for member in self.client.get_chat_members(self.chat_id):
                if member.user.is_deleted:
                    await self.kick_member(member.user.id)
                    self.kicked_count += 1
        except Exception as e:
            return await self.message.edit(format_exc(e))
        await self.message.edit(
            f"<b>Successfully kicked {self.kicked_count} deleted account(s)</b>",
        )

    async def kick_member(self, user_id):
        try:
            await self.client.ban_chat_member(
                self.chat_id, user_id, datetime.now() + timedelta(seconds=31)
            )
        except Exception as e:
            await self.message.edit(f"Failed to kick user {user_id}: {format_exc(e)}")
