import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from helper.helper_func import encode

#===============================================================#

def get_custom_buttons(client, link):
    """Custom buttons banao - agar set hain to"""
    buttons = []
    if hasattr(client, 'custom_buttons') and client.custom_buttons:
        for name, data in client.custom_buttons.items():
            parts = data.split("|")
            btn_text = parts[0]
            btn_url = parts[1] if len(parts) > 1 else link
            buttons.append([InlineKeyboardButton(btn_text, url=btn_url)])
    else:
        # Koi custom button nahi hai to khaali markup
        pass
    return buttons

#===============================================================#


#===============================================================#

@Client.on_message(filters.private & filters.command('getlink'))
async def getlink_command(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply(client.reply_text)
    
    if not message.reply_to_message:
        return await message.reply("**⚠️ How to use /getlink:**\n\n1. Forward any file to this bot\n2. Reply to that forwarded file\n3. Send /getlink in the reply\n\nThen bot will generate a link for that file!")
    
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        post_message = await message.reply_to_message.copy(chat_id=client.db, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.reply_to_message.copy(chat_id=client.db, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    
    converted_id = post_message.id * abs(client.db)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    # Admin ko Share URL dikhao
    admin_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=admin_markup, disable_web_page_preview=True)

    # File pe custom buttons lagao
    if not client.disable_btn:
        custom_btns = get_custom_buttons(client, link)
        if custom_btns:
            await post_message.edit_reply_markup(InlineKeyboardMarkup(custom_btns))

#===============================================================#

@Client.on_message(filters.channel & filters.incoming)
async def new_post(client: Client, message: Message):
    if message.chat.id != client.db:
        return
    if client.disable_btn:
        return

    converted_id = message.id * abs(client.db)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    
    custom_btns = get_custom_buttons(client, link)
    if custom_btns:
        try:
            await message.edit_reply_markup(InlineKeyboardMarkup(custom_btns))
        except Exception as e:
            print(e)
            pass
    
