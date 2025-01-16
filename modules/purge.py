from pyrogram import Client, filters
from pyrogram.enums import ChatType

from utils.misc import prefix

@Client.on_message(filters.command(["purge", "del"], prefix) & filters.me)
async def purge(client: Client, message: Message):
    async with client:
        async for dialog in client.get_dialogs():
            if dialog.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
                print("Cleaning Messages in Group:{}...".format(dialog.chat.title))
                async for message in client.search_messages(chat_id=dialog.chat.id, from_user="me"):
                    if message.text:
                        print("Deleting Message Contents:{}...".format(message.text))
                    await client.delete_messages(chat_id=dialog.chat.id, message_ids=message.id)

