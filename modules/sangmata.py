import asyncio

from pyrogram import Client, enums, filters
from pyrogram.types import Message
from pyrogram.errors import RPCError

from utils.misc import modules_help, prefix
from utils.scripts import edit_or_reply


@Client.on_message(filters.command("cek", prefix) & filters.me)
async def sg(client: Client, message: Message):
    lol = await edit_or_reply(message, "<code>sedang memproses, tunggu...</code>")
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id
    else:
        await message.edit(f"<b>Cara menggunakan: </b><code>{prefix}cek [reply]</code>")
        return
    try:
        await client.send_message(
            "@SangMata_beta_bot", "/start", parse_mode=enums.ParseMode.MARKDOWN
        )
    except RPCError:
        await lol.edit(
            "**Buka blokir @SangMata_beta_bot dan coba lagi**",
            parse_mode=enums.ParseMode.MARKDOWN,
        )
        return
    id = "@SangMata_beta_bot"
    chat = message.chat.id
    await client.send_message(id, user_id, parse_mode=enums.ParseMode.MARKDOWN)
    await asyncio.sleep(2)
    async for opt in client.get_chat_history("@SangMata_beta_bot", limit=1):
        hmm = opt.text
        if hmm.startswith("Forward"):
            await lol.edit(
                "**Unknown error occurred**", parse_mode=enums.ParseMode.MARKDOWN
            )
            return
        await lol.delete()
        await opt.copy(chat)


modules_help["sangmata"] = {"cek": "cek riwayat akun telegram"}
