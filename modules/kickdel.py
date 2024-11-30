from pyrogram import Client, ContinuePropagation, filters
from pyrogram.types import Message, ChatPermissions
from utils.db import db
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


@Client.on_message(filters.command(["kd"], prefix) & filters.me)
async def kickdel_cmd(client: Client, message: Message):
    handler = KickDeletedAccountsHandler(client, message)
    await handler.kick_deleted_accounts()


modules_help["kickdel"] = {
    "kd": "Kick all deleted accounts",
}
