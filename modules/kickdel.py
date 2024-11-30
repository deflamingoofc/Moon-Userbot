from pyrogram import Client, filters

from pyrogram.errors import (
    UserAdminInvalid,
    ChatAdminRequired,
    RPCError,
)

from pyrogram.types import Message, ChatPermissions

from utils.misc import modules_help, prefix
from utils.handlers import (
    KickDeletedAccountsHandler,
)


@Client.on_message(filters.command(["kd"], prefix) & filters.me)
async def kickdel_cmd(client: Client, message: Message):
    handler = KickDeletedAccountsHandler(client, message)
    await handler.kick_deleted_accounts()


modules_help["kickdel"] = {
    "kd": "Kick all deleted accounts",
}
