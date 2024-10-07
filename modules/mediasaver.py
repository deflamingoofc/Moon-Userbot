from pyrogram import Client, filters, enums
from pyrogram.types import Message

from utils.misc import modules_help


@Client.on_message(filters.private & filters.incoming & ~filters.service & ~filters.me & ~filters.bot)
async def msave(client: Client, message: Message):
    media = message.media
    await client.send_document("me", parse_mode=enums.ParseMode.DISABLE)


modules_help["mediasaver"] = {
    "s": "Save self-destructing media and send it to Saved Messages",
}
