from aiopath import AsyncPath

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from utils.misc import modules_help


@Client.on_message(
    ~filters.me & (filters.private)
)
async def incoming_msg_handler(client: Client, msg: Message) -> None:
    saved_msg, user, chat = None, msg.from_user, msg.chat
    media_type = msg.media.value
    download_path = AsyncPath(await client.download_media(msg))
    send_method = getattr(client, f"send_{media_type}", None)
    saved_msg = await send_method(
        "self",
        download_path,
        caption=msg.caption or None,
        caption_entities=(
            msg.caption.entities
            if msg.caption and msg.caption.entities
            else None
        ),
    )
    await download_path.unlink()

modules_help["msg"] = {
    "msg": "simply run or reply to message",
}
