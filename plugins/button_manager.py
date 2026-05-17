from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.pyromod import ListenerTimeout

# Button data store: {name: button_text}
# Stored in client.custom_buttons = {"Button Name": "Button Text|URL"}

#===============================================================#

async def set_button_menu(client, query):
    """Show Set Button main menu"""
    if query.from_user.id != client.owner:
        return await query.answer("❌ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!", show_alert=True)

    if not hasattr(client, 'custom_buttons'):
        client.custom_buttons = {}

    buttons_list = ""
    if client.custom_buttons:
        for i, (name, data) in enumerate(client.custom_buttons.items(), 1):
            parts = data.split("|")
            btn_text = parts[0]
            btn_url = parts[1] if len(parts) > 1 else "No URL"
            buttons_list += f"\n{i}. **{name}**\n   📝 Text: `{btn_text}`\n   🔗 URL: `{btn_url}`\n"
    else:
        buttons_list = "\n_ᴀʙʜɪ ᴋᴏɪ ʙᴜᴛᴛᴏɴ sᴇᴛ ɴᴀʜɪɴ ʜᴀɪ_"

    msg = f"""<blockquote>🔘 **sᴇᴛ ʙᴜᴛᴛᴏɴ ᴍᴀɴᴀɢᴇʀ**</blockquote>

**sᴀᴠᴇᴅ ʙᴜᴛᴛᴏɴs:**{buttons_list}

__ɴᴇᴡ ʙᴜᴛᴛᴏɴ ʙᴀɴᴀɴᴇ ᴋᴇ ʟɪʏᴇ ➕ ᴀᴅᴅ ʙᴜᴛᴛᴏɴ ᴅᴀʙᴀᴏ__
__ᴇᴅɪᴛ ʏᴀ ᴅᴇʟᴇᴛᴇ ᴋᴇ ʟɪʏᴇ ʙᴜᴛᴛᴏɴ ɴᴀᴍ ᴅᴀʟᴏ__"""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('➕ ᴀᴅᴅ ʙᴜᴛᴛᴏɴ', 'add_custom_button')],
        [InlineKeyboardButton('✏️ ᴇᴅɪᴛ ʙᴜᴛᴛᴏɴ', 'edit_custom_button'), InlineKeyboardButton('🗑️ ᴅᴇʟᴇᴛᴇ ʙᴜᴛᴛᴏɴ', 'delete_custom_button')],
        [InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'settings_page_2')]
    ])
    await query.message.edit_text(msg, reply_markup=reply_markup)

#===============================================================#

@Client.on_callback_query(filters.regex("^set_button_menu$"))
async def set_button_menu_cb(client, query):
    if query.from_user.id != client.owner:
        return await query.answer("❌ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!", show_alert=True)
    await set_button_menu(client, query)

#===============================================================#

@Client.on_callback_query(filters.regex("^add_custom_button$"))
async def add_custom_button(client, query):
    if query.from_user.id != client.owner:
        return await query.answer("❌ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!", show_alert=True)

    await query.answer()
    guide_msg = """<blockquote>➕ **ɴʏᴀ ʙᴜᴛᴛᴏɴ ᴀᴅᴅ ᴋᴀʀᴏ**</blockquote>

**ɴɪᴄʜᴇ ᴅɪʏᴇ ꜰᴏʀᴍᴀᴛ ᴍᴇɪɴ ʙʜᴇᴊᴏ:**

```
NAME | BUTTON TEXT | URL
```

**ᴜᴅᴀʜᴀʀᴀɴ:**
```
Join Button | 📢 Join Now | https://t.me/yourchannel
```
```
Website | 🌐 Visit Site | https://example.com
```

**ʀᴜʟᴇs:**
• `NAME` — ʙᴜᴛᴛᴏɴ ᴋᴀ ɴᴀᴍ (ᴀᴀᴘᴋᴇ ʟɪʏᴇ ᴘᴀʜᴄʜᴀɴ ᴋᴇ ʟɪʏᴇ)
• `BUTTON TEXT` — ʙᴜᴛᴛᴏɴ ᴘᴇ ᴅɪᴋʜɴᴇ ᴠᴀʟᴀ ᴛᴇxᴛ
• `URL` — ʙᴜᴛᴛᴏɴ ᴋᴀ ʟɪɴᴋ

`0` ʙʜᴇᴊᴏ ᴛᴏ ᴄᴀɴᴄᴇʟ ʜᴏɢᴀ | 60 ꜱᴇᴄᴏɴᴅ ᴍᴇɪɴ ʙʜᴇᴊᴏ"""

    await query.message.edit_text(guide_msg)

    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        text = res.text.strip()

        if text == '0':
            return await query.message.edit_text("❌ **ᴄᴀɴᴄᴇʟ ᴋɪʏᴀ ɢᴀʏᴀ!**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

        parts = [p.strip() for p in text.split('|')]
        if len(parts) != 3:
            return await query.message.edit_text(
                "❌ **ɢʟᴀᴛ ꜰᴏʀᴍᴀᴛ!**\n\n**sʜɪ ꜰᴏʀᴍᴀᴛ:**\n`NAME | BUTTON TEXT | URL`",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

        name, btn_text, url = parts

        if not url.startswith('http'):
            return await query.message.edit_text(
                "❌ **URL sʜɪ ɴᴀʜɪɴ ʜᴀɪ!**\n`http://` ʏᴀ `https://` ꜱᴇ ꜱʜᴜʀᴜ ʜᴏɴᴀ ᴄʜᴀʜɪʏᴇ!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

        if not hasattr(client, 'custom_buttons'):
            client.custom_buttons = {}

        client.custom_buttons[name] = f"{btn_text}|{url}"

        await query.message.edit_text(
            f"✅ **ʙᴜᴛᴛᴏɴ ꜱᴀᴠᴇ ʜᴏ ɢᴀʏᴀ!**\n\n📝 **ɴᴀᴍ:** `{name}`\n🔘 **ʙᴜᴛᴛᴏɴ ᴛᴇxᴛ:** `{btn_text}`\n🔗 **URL:** `{url}`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

    except ListenerTimeout:
        return await query.message.edit_text("⏰ **ᴛᴀɪᴍᴀᴜᴛ!** ᴅᴏʙᴀʀᴀ ᴋᴏꜱʜɪꜱʜ ᴋᴀʀᴏ!",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^edit_custom_button$"))
async def edit_custom_button(client, query):
    if query.from_user.id != client.owner:
        return await query.answer("❌ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!", show_alert=True)

    if not hasattr(client, 'custom_buttons') or not client.custom_buttons:
        return await query.answer("⚠️ ᴋᴏɪ ʙᴜᴛᴛᴏɴ ɴᴀʜɪɴ ʜᴀɪ!", show_alert=True)

    await query.answer()
    buttons_list = "\n".join([f"• `{name}`" for name in client.custom_buttons.keys()])

    await query.message.edit_text(
        f"✏️ **ᴋᴏɴꜱᴀ ʙᴜᴛᴛᴏɴ ᴇᴅɪᴛ ᴋᴀʀᴇɴ?**\n\n{buttons_list}\n\n__ʙᴜᴛᴛᴏɴ ᴋᴀ ɴᴀᴍ ʙʜᴇᴊᴏ ᴊᴏ ᴇᴅɪᴛ ᴋᴀʀɴᴀ ʜᴀɪ | `0` ᴄᴀɴᴄᴇʟ ᴋᴇ ʟɪʏᴇ__")

    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        name = res.text.strip()

        if name == '0':
            return await query.message.edit_text("❌ ᴄᴀɴᴄᴇʟ!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

        if name not in client.custom_buttons:
            return await query.message.edit_text(f"❌ **`{name}` ʏᴇ ɴᴀᴍ ɴᴀʜɪɴ ᴍɪʟᴀ!**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

        old_data = client.custom_buttons[name].split("|")
        old_text = old_data[0]
        old_url = old_data[1] if len(old_data) > 1 else ""

        await query.message.edit_text(
            f"✏️ **ɴʏᴀ ᴅᴀᴛᴀ ʙʜᴇᴊᴏ:**\n\n**ᴘᴜʀᴀɴᴀ:**\n📝 Text: `{old_text}`\n🔗 URL: `{old_url}`\n\n**ꜰᴏʀᴍᴀᴛ:**\n`BUTTON TEXT | URL`\n\n`0` ᴄᴀɴᴄᴇʟ ᴋᴇ ʟɪʏᴇ")

        res2 = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        new_data = res2.text.strip()

        if new_data == '0':
            return await query.message.edit_text("❌ ᴄᴀɴᴄᴇʟ!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

        parts = [p.strip() for p in new_data.split('|')]
        if len(parts) != 2:
            return await query.message.edit_text("❌ **ɢʟᴀᴛ ꜰᴏʀᴍᴀᴛ!** `BUTTON TEXT | URL`",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

        new_text, new_url = parts
        client.custom_buttons[name] = f"{new_text}|{new_url}"

        await query.message.edit_text(
            f"✅ **ʙᴜᴛᴛᴏɴ ᴀᴘᴅᴇᴛ ʜᴏ ɢᴀʏᴀ!**\n\n📝 **ɴᴀᴍ:** `{name}`\n🔘 **ɴʏᴀ ᴛᴇxᴛ:** `{new_text}`\n🔗 **ɴʏᴀ URL:** `{new_url}`",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

    except ListenerTimeout:
        return await query.message.edit_text("⏰ **ᴛᴀɪᴍᴀᴜᴛ!**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

#===============================================================#

@Client.on_callback_query(filters.regex("^delete_custom_button$"))
async def delete_custom_button(client, query):
    if query.from_user.id != client.owner:
        return await query.answer("❌ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!", show_alert=True)

    if not hasattr(client, 'custom_buttons') or not client.custom_buttons:
        return await query.answer("⚠️ ᴋᴏɪ ʙᴜᴛᴛᴏɴ ɴᴀʜɪɴ ʜᴀɪ!", show_alert=True)

    await query.answer()
    buttons_list = "\n".join([f"• `{name}`" for name in client.custom_buttons.keys()])

    await query.message.edit_text(
        f"🗑️ **ᴋᴏɴꜱᴀ ʙᴜᴛᴛᴏɴ ᴅᴇʟᴇᴛᴇ ᴋᴀʀᴇɴ?**\n\n{buttons_list}\n\n__ɴᴀᴍ ʙʜᴇᴊᴏ | `0` ᴄᴀɴᴄᴇʟ ᴋᴇ ʟɪʏᴇ__")

    try:
        res = await client.listen(user_id=query.from_user.id, filters=filters.text, timeout=60)
        name = res.text.strip()

        if name == '0':
            return await query.message.edit_text("❌ ᴄᴀɴᴄᴇʟ!",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

        if name not in client.custom_buttons:
            return await query.message.edit_text(f"❌ **`{name}` ɴᴀᴍ ɴᴀʜɪɴ ᴍɪʟᴀ!**",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

        del client.custom_buttons[name]
        await query.message.edit_text(f"✅ **`{name}` ʙᴜᴛᴛᴏɴ ᴅᴇʟᴇᴛᴇ ʜᴏ ɢᴀʏᴀ!**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))

    except ListenerTimeout:
        return await query.message.edit_text("⏰ **ᴛᴀɪᴍᴀᴜᴛ!**",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('◂ ʙᴀᴄᴋ', 'set_button_menu')]]))
            
