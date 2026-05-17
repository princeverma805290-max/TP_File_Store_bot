from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helper.helper_func import encode, get_message_id
from config import LOGGER

async def get_db_channels_info(client):
    """Get formatted database channels information with links"""
    db_channels = getattr(client, 'db_channels', {})
    primary_db = getattr(client, 'primary_db_channel', client.db)
    
    if not db_channels:
        # If no additional DB channels, show primary only
        try:
            primary_chat = await client.get_chat(primary_db)
            if hasattr(primary_chat, 'invite_link') and primary_chat.invite_link:
                return f"<blockquote>✦ ᴘʀɪᴍᴀʀʏ ᴅʙ ᴄʜᴀɴɴᴇʟ: <a href='{primary_chat.invite_link}'>{primary_chat.title}</a></blockquote>"
            else:
                return f"<blockquote>✦ ᴘʀɪᴍᴀʀʏ ᴅʙ ᴄʜᴀɴɴᴇʟ: {primary_chat.title} (`{primary_db}`)</blockquote>"
        except:
            return f"<blockquote>✦ ᴘʀɪᴍᴀʀʏ ᴅʙ ᴄʜᴀɴɴᴇʟ: `{primary_db}`</blockquote>"
    
    # Format all DB channels with links
    channels_info = ["<blockquote>✦ ᴀᴠᴀɪʟᴀʙʟᴇ ᴅᴀᴛᴀʙᴀsᴇ ᴄʜᴀɴɴᴇʟs:</blockquote>"]
    for channel_id_str, channel_data in db_channels.items():
        channel_name = channel_data.get('name', 'ᴜɴᴋɴᴏᴡɴ')
        is_primary_text = "✦ ᴘʀɪᴍᴀʀʏ" if channel_data.get('is_primary', False) else "• sᴇᴄᴏɴᴅᴀʀʏ"
        
        try:
            chat = await client.get_chat(int(channel_id_str))
            if hasattr(chat, 'invite_link') and chat.invite_link:
                channels_info.append(f"{is_primary_text}: <a href='{chat.invite_link}'>{channel_name}</a>")
            else:
                channels_info.append(f"{is_primary_text}: {channel_name} (`{channel_id_str}`)")
        except:
            channels_info.append(f"{is_primary_text}: {channel_name} (`{channel_id_str}`)")
    
    return "\n".join(channels_info)

@Client.on_message(filters.private & filters.command('batch'))
async def batch(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply(client.reply_text)

    user_id = message.from_user.id

    # Initialize batch storage
    if not hasattr(client, 'batch_files'):
        client.batch_files = {}
    client.batch_files[user_id] = []

    status_msg = await message.reply(
        "<blockquote>📦 **ʙᴀᴛᴄʜ ᴍᴏᴅᴇ ᴀᴄᴛɪᴠᴇ**</blockquote>\n\n"
        "✅ ᴀʙ ᴊɪᴛɴɪ ʙʜɪ ꜰɪʟᴇs ᴄʜᴀʜɪʏᴇ ʙᴏᴛ ᴘᴇ ꜰᴏʀᴡᴀʀᴅ ᴋᴀʀᴏ\n"
        "📁 ꜰɪʟᴇs ᴀᴅᴅᴇᴅ: **0**\n\n"
        "⬇️ ᴊᴀʙ ʜᴏ ᴊᴀᴀʏᴇ ᴛᴀʙ ɴɪᴄʜᴇ ʙᴜᴛᴛᴏɴ ᴅᴀʙᴀᴏ:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ ɢᴇɴᴇʀᴀᴛᴇ ʟɪɴᴋ", callback_data=f"batch_generate_{user_id}")],
            [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data=f"batch_close_{user_id}")]
        ])
    )

    # Store status message id
    if not hasattr(client, 'batch_status_msg'):
        client.batch_status_msg = {}
    client.batch_status_msg[user_id] = status_msg

#===============================================================#

@Client.on_message(filters.private & filters.forwarded)
async def batch_collect(client: Client, message: Message):
    user_id = message.from_user.id
    if not hasattr(client, 'batch_files') or user_id not in client.batch_files:
        return
    if user_id not in client.admins:
        return

    try:
        # Copy file to DB channel
        from pyrogram.errors import FloodWait
        import asyncio
        try:
            post_message = await message.copy(chat_id=client.db, disable_notification=True)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            post_message = await message.copy(chat_id=client.db, disable_notification=True)

        client.batch_files[user_id].append(post_message.id)
        count = len(client.batch_files[user_id])

        # Update status message
        status_msg = client.batch_status_msg.get(user_id)
        if status_msg:
            await status_msg.edit_text(
                "<blockquote>📦 **ʙᴀᴛᴄʜ ᴍᴏᴅᴇ ᴀᴄᴛɪᴠᴇ**</blockquote>\n\n"
                "✅ ᴀʙ ᴊɪᴛɴɪ ʙʜɪ ꜰɪʟᴇs ᴄʜᴀʜɪʏᴇ ʙᴏᴛ ᴘᴇ ꜰᴏʀᴡᴀʀᴅ ᴋᴀʀᴏ\n"
                f"📁 ꜰɪʟᴇs ᴀᴅᴅᴇᴅ: **{count}**\n\n"
                "⬇️ ᴊᴀʙ ʜᴏ ᴊᴀᴀʏᴇ ᴛᴀʙ ɴɪᴄʜᴇ ʙᴜᴛᴛᴏɴ ᴅᴀʙᴀᴏ:",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ ɢᴇɴᴇʀᴀᴛᴇ ʟɪɴᴋ", callback_data=f"batch_generate_{user_id}")],
                    [InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data=f"batch_close_{user_id}")]
                ])
            )
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

#===============================================================#

@Client.on_callback_query(filters.regex(r"^batch_generate_(\d+)$"))
async def batch_generate(client: Client, query):
    user_id = int(query.matches[0].group(1))

    if query.from_user.id != user_id:
        return await query.answer("❌ ʏᴇ ᴀᴀᴘᴋᴀ ʙᴀᴛᴄʜ ɴᴀʜɪɴ ʜᴀɪ!", show_alert=True)

    if not hasattr(client, 'batch_files') or user_id not in client.batch_files:
        return await query.answer("❌ ᴋᴏɪ ꜰɪʟᴇ ɴᴀʜɪɴ ʜᴀɪ!", show_alert=True)

    files = client.batch_files[user_id]
    if not files:
        return await query.answer("❌ ᴋᴏɪ ꜰɪʟᴇ ꜰᴏʀᴡᴀʀᴅ ɴᴀʜɪɴ ᴋɪ!", show_alert=True)

    first_id = files[0]
    last_id = files[-1]

    string = f"get-{first_id * abs(client.db)}-{last_id * abs(client.db)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    # Clear batch data
    client.batch_files.pop(user_id, None)
    client.batch_status_msg.pop(user_id, None)

    await query.message.edit_text(
        f"<blockquote>✓ ʙᴀᴛᴄʜ ʟɪɴᴋ ʀᴇᴀᴅʏ!</blockquote>\n\n"
        f"📁 ᴛᴏᴛᴀʟ ꜰɪʟᴇs: **{len(files)}**\n\n"
        f"<code>{link}</code>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 sʜᴀʀᴇ ᴜʀʟ", url=f'https://telegram.me/share/url?url={link}')]
        ])
    )

#===============================================================#

@Client.on_callback_query(filters.regex(r"^batch_close_(\d+)$"))
async def batch_close(client: Client, query):
    user_id = int(query.matches[0].group(1))

    if query.from_user.id != user_id:
        return await query.answer("❌ ʏᴇ ᴀᴀᴘᴋᴀ ʙᴀᴛᴄʜ ɴᴀʜɪɴ ʜᴀɪ!", show_alert=True)

    # Clear batch data
    if hasattr(client, 'batch_files'):
        client.batch_files.pop(user_id, None)
    if hasattr(client, 'batch_status_msg'):
        client.batch_status_msg.pop(user_id, None)

    await query.message.edit_text("❌ **ʙᴀᴛᴄʜ ᴄᴀɴᴄᴇʟ ʜᴏ ɢᴀʏᴀ!**")

#===============================================================#

@Client.on_message(filters.private & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply(client.reply_text)
    
    # Get all database channels with links
    db_channels_info = await get_db_channels_info(client)
    
    while True:
        try:
            channel_message = await client.ask(
                text=f"""<blockquote>ꜰᴏʀᴡᴀʀᴅ ᴍᴇssᴀɢᴇ ꜰʀᴏᴍ ᴛʜᴇ ᴅʙ ᴄʜᴀɴɴᴇʟ (ᴡɪᴛʜ ǫᴜᴏᴛᴇs)..</blockquote>

{db_channels_info}

<blockquote>ᴏʀ sᴇɴᴅ ᴛʜᴇ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ʟɪɴᴋ</blockquote>""",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        msg_id, source_channel_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("<blockquote>✗ ᴇʀʀᴏʀ</blockquote>\n\nᴛʜɪs ꜰᴏʀᴡᴀʀᴅᴇᴅ ᴘᴏsᴛ ɪs ɴᴏᴛ ꜰʀᴏᴍ ᴍʏ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴏʀ ᴛʜɪs ʟɪɴᴋ ɪs ɴᴏᴛ ᴛᴀᴋᴇɴ ꜰʀᴏᴍ ᴅʙ ᴄʜᴀɴɴᴇʟ", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(source_channel_id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 sʜᴀʀᴇ ᴜʀʟ", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<blockquote>✓ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ</blockquote>\n\n<code>{link}</code>", quote=True, reply_markup=reply_markup)

#===============================================================#

@Client.on_message(filters.private & filters.command("nbatch"))
async def nbatch(client: Client, message: Message):
    if message.from_user.id not in client.admins:
        return await message.reply(client.reply_text)
    
    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        await message.reply("<blockquote>✗ ɪɴᴠᴀʟɪᴅ ꜰᴏʀᴍᴀᴛ!</blockquote> ᴜsᴇ: /nbatch {number}")
        return
    
    batch_size = int(args[1])
    
    # Get all database channels with links
    db_channels_info = await get_db_channels_info(client)
    
    while True:
        try:
            first_message = await client.ask(
                text=f"""<blockquote>🚀 sᴇɴᴅ ᴅʙ ᴄʜᴀɴɴᴇʟ ꜰɪʀsᴛ ᴍᴇssᴀɢᴇ ʟɪɴᴋ (ᴡɪᴛʜ ǫᴜᴏᴛᴇs)...</blockquote>

{db_channels_info}""",
                chat_id=message.from_user.id,
                filters=(filters.text & ~filters.forwarded),
                timeout=60
            )
        except:
            return
    
        f_msg_id, source_channel_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("<blockquote>😫 ɪɴᴠᴀʟɪᴅ!</blockquote> sᴇɴᴅ ᴄᴏʀʀᴇᴄᴛ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴍᴇssᴀɢᴇ ʟɪɴᴋ.", quote=True)
            continue
    
    s_msg_id = f_msg_id + batch_size - 1  # Adding batch_size to first message ID
    
    string = f"get-{f_msg_id * abs(source_channel_id)}-{s_msg_id * abs(source_channel_id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📫 ʏᴏᴜʀ ʙᴀᴛᴄʜ ᴜʀʟ", url=f'https://telegram.me/share/url?url={link}')]
    ])
    
    await first_message.reply_text(f"<blockquote>✓ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʙᴀᴛᴄʜ ʟɪɴᴋ</blockquote>\n\n<code>{link}</code>", quote=True, reply_markup=reply_markup)    
                
