from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("terima", prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    chat_id = message.chat.id
    await client.approve_all_chat_join_requests(chat_id)
    await message.edit_text("Selesai")
    await message.delete()

modules_help["terima"] = {
    "terima": "terima semua yang meminta untuk bergabung",
}
