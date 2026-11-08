import pytz
import datetime
import os
import asyncio

from Script import script
from info import *
from utils import get_seconds, temp
from database.users_chats_db import db

from pyrogram import Client, filters
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import *


# --- ENVIRONMENTAL VARIABLES ---
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "AmarSingh820")
PREMIUM_PIC = os.environ.get(
    "START_PIC",
    "https://i.postimg.cc/j2nLk6yb/file-000000009aec7206bfa30465434fd82a.png"
)
# --------------------------------


# Remove Premium
@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)

        if await db.remove_premium_access(user_id):
            await message.reply_text(
                "ᴜꜱᴇʀ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ !"
            )

            await client.send_message(
                chat_id=user_id,
                text=script.PREMIUM_END_TEXT.format(user.mention)
            )
        else:
            await message.reply_text(
                "ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴜꜱᴇᴅ !\n"
                "ᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ, ɪᴛ ᴡᴀꜱ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ɪᴅ ?"
            )
    else:
        await message.reply_text(
            "ᴜꜱᴀɢᴇ : /remove_premium user_id"
        )


# My Premium Plan
@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    try:
        user = message.from_user.mention
        user_id = message.from_user.id
        data = await db.get_user(user_id)

        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time")

            expiry_ist = expiry.astimezone(
                pytz.timezone("Asia/Kolkata")
            )

            expiry_str_in_ist = expiry_ist.strftime(
                "%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p"
            )

            current_time = datetime.datetime.now(
                pytz.timezone("Asia/Kolkata")
            )

            time_left = expiry_ist - current_time

            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_left_str = (
                f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, "
                f"{minutes} ᴍɪɴᴜᴛᴇꜱ"
            )

            caption = (
                f"⚜️ <b>ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :</b>\n\n"
                f"👤 <b>ᴜꜱᴇʀ :</b> {user}\n"
                f"⚡ <b>ᴜꜱᴇʀ ɪᴅ :</b> <code>{user_id}</code>\n"
                f"⏰ <b>ᴛɪᴍᴇ ʟᴇꜰᴛ :</b> {time_left_str}\n"
                f"⌛️ <b>ᴇxᴘɪʀʏ ᴅᴀᴛᴇ :</b> {expiry_str_in_ist}"
            )

            await message.reply_photo(
                photo=PREMIUM_PIC,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            "🔥 ᴇxᴛᴇɴᴅ ᴘʟᴀɴ",
                            callback_data="premium_info"
                        )
                    ]]
                )
            )

        else:
            await message.reply_photo(
                photo=PREMIUM_PIC,
                caption=(
                    f"<b>ʜᴇʏ {user},\n\n"
                    f"ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ.\n"
                    f"ʙᴜʏ ᴏᴜʀ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ ᴛᴏ ᴇɴᴊᴏʏ "
                    f"ᴘʀᴇᴍɪᴜᴍ ʙᴇɴᴇꜰɪᴛꜱ.</b>"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [[
                        InlineKeyboardButton(
                            "💎 ᴄʜᴇᴄᴋᴏᴜᴛ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ",
                            callback_data="premium_info"
                        )
                    ]]
                )
            )

    except Exception as e:
        print(e)


# Get Premium Details
@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await db.get_user(user_id)

        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time")

            expiry_ist = expiry.astimezone(
                pytz.timezone("Asia/Kolkata")
            )

            expiry_str_in_ist = expiry_ist.strftime(
                "%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p"
            )

            current_time = datetime.datetime.now(
                pytz.timezone("Asia/Kolkata")
            )

            time_left = expiry_ist - current_time

            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_left_str = (
                f"{days} days, {hours} hours, {minutes} minutes"
            )

            await message.reply_text(
                f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n"
                f"👤 ᴜꜱᴇʀ : {user.mention}\n"
                f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
                f"⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n"
                f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}"
            )

        else:
            await message.reply_text(
                "ɴᴏ ᴀɴʏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ᴏꜰ ᴛʜᴇ ᴜꜱᴇʀ "
                "ᴡᴀꜱ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ !"
            )

    else:
        await message.reply_text(
            "ᴜꜱᴀɢᴇ : /get_premium user_id"
        )


# Add Premium to One User
@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(
            pytz.timezone("Asia/Kolkata")
        )

        current_time = time_zone.strftime(
            "%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p"
        )

        user_id = int(message.command[1])
        user = await client.get_users(user_id)

        time = message.command[2] + " " + message.command[3]
        seconds = await get_seconds(time)

        if seconds > 0:
            expiry_time = (
                datetime.datetime.now()
                + datetime.timedelta(seconds=seconds)
            )

            user_data = {
                "id": user_id,
                "expiry_time": expiry_time
            }

            await db.update_user(user_data)

            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")

            expiry_str_in_ist = expiry.astimezone(
                pytz.timezone("Asia/Kolkata")
            ).strftime(
                "%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p"
            )

            await message.reply_text(
                f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅\n\n"
                f"👤 ᴜꜱᴇʀ : {user.mention}\n"
                f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
                f"⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n\n"
                f"⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n"
                f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}",
                disable_web_page_preview=True
            )

            await client.send_message(
                chat_id=user_id,
                text=(
                    f"👋 ʜᴇʏ {user.mention},\n"
                    f"ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴘᴜʀᴄʜᴀꜱɪɴɢ ᴘʀᴇᴍɪᴜᴍ.\n"
                    f"ᴇɴᴊᴏʏ !! ✨🎉\n\n"
                    f"⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n"
                    f"⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n"
                    f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}"
                ),
                disable_web_page_preview=True
            )

            await client.send_message(
                PREMIUM_LOGS,
                text=(
                    f"#Added_Premium\n\n"
                    f"👤 ᴜꜱᴇʀ : {user.mention}\n"
                    f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
                    f"⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time}</code>\n\n"
                    f"⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n"
                    f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}"
                ),
                disable_web_page_preview=True
            )

        else:
            await message.reply_text(
                "❌ ɪɴᴠᴀʟɪᴅ ᴛɪᴍᴇ ꜰᴏʀᴍᴀᴛ ❗\n"
                "🕒 ᴘʟᴇᴀsᴇ ᴜsᴇ: <code>1 day</code>, "
                "<code>1 hour</code>, <code>1 min</code>, "
                "<code>1 month</code>, or <code>1 year</code>"
            )

    else:
        await message.reply_text(
            "📌 ᴜsᴀɢᴇ: <code>/add_premium user_id time</code>\n"
            "📅 ᴇxᴀᴍᴘʟᴇ: <code>/add_premium 123456 1 month</code>\n"
            "🧭 ᴀᴄᴄᴇᴘᴛᴇᴅ ꜰᴏʀᴍᴀᴛs: <code>1 day</code>, "
            "<code>1 hour</code>, <code>1 min</code>, "
            "<code>1 month</code>, <code>1 year</code>"
        )


# Premium Users List
@Client.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("<i>ꜰᴇᴛᴄʜɪɴɢ...</i>")

    new = " ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ ʟɪꜱᴛ :\n\n"
    user_count = 1

    users = await db.get_all_users()

    async for user in users:
        data = await db.get_user(user["id"])

        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time")

            expiry_ist = expiry.astimezone(
                pytz.timezone("Asia/Kolkata")
            )

            expiry_str_in_ist = expiry_ist.strftime(
                "%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p"
            )

            current_time = datetime.datetime.now(
                pytz.timezone("Asia/Kolkata")
            )

            time_left = expiry_ist - current_time

            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            time_left_str = (
                f"{days} days, {hours} hours, {minutes} minutes"
            )

            new += (
                f"{user_count}. {(await client.get_users(user['id'])).mention}\n"
                f"👤 ᴜꜱᴇʀ ɪᴅ : {user['id']}\n"
                f"⏳ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}\n"
                f"⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n"
            )

            user_count += 1

    try:
        await aa.edit_text(new)

    except MessageTooLong:
        with open("usersplan.txt", "w+") as outfile:
            outfile.write(new)

        await message.reply_document(
            "usersplan.txt",
            caption="Paid Users:"
        )


# Plan Menu
@Client.on_message(filters.command("plan"))
async def plan(client, message):
    user_id = message.from_user.id
    users = message.from_user.mention

    log_message = (
        f"<b><u>🚫 ᴛʜɪs ᴜsᴇʀs ᴛʀʏ ᴛᴏ ᴄʜᴇᴄᴋ /plan</u> "
        f"{temp.B_LINK}\n\n"
        f"- ɪᴅ - `{user_id}`\n"
        f"- ɴᴀᴍᴇ - {users}</b>"
    )

    btn = [
        [
            InlineKeyboardButton(
                "• ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •",
                callback_data="buy_info"
            )
        ],
        [
            InlineKeyboardButton(
                "• ʀᴇꜰᴇʀ ꜰʀɪᴇɴᴅꜱ",
                callback_data="reffff"
            ),
            InlineKeyboardButton(
                "ꜰʀᴇᴇ ᴛʀɪᴀʟ •",
                callback_data="free"
            )
        ],
        [
            InlineKeyboardButton(
                "🚫 ᴄʟᴏꜱᴇ 🚫",
                callback_data="close_data"
            )
        ]
    ]

    msg = await message.reply_photo(
        photo=PREMIUM_PIC,
        caption=script.BPREMIUM_TXT,
        reply_markup=InlineKeyboardMarkup(btn)
    )

    await client.send_message(
        PREMIUM_LOGS,
        log_message
    )

    await asyncio.sleep(300)

    await msg.delete()
    await message.delete()


# Telegram Star Payment Method
# Credit - @BeingXAnonymous

@Client.on_callback_query(filters.regex(r"buy_\d+"))
async def premium_button(client, callback_query: CallbackQuery):
    try:
        amount = int(callback_query.data.split("_")[1])

        if amount in STAR_PREMIUM_PLANS:
            try:
                buttons = [[
                    InlineKeyboardButton(
                        "ᴄᴀɴᴄᴇʟ 🚫",
                        callback_data="close_data"
                    )
                ]]

                reply_markup = InlineKeyboardMarkup(buttons)

                await client.send_invoice(
                    chat_id=callback_query.message.chat.id,
                    title="Premium Subscription",
                    description=(
                        f"Pay {amount} Star And Get Premium For "
                        f"{STAR_PREMIUM_PLANS[amount]}"
                    ),
                    payload=f"dreamxpremium_{amount}",
                    currency="XTR",
                    prices=[
                        LabeledPrice(
                            label="Premium Subscription",
                            amount=amount
                        )
                    ],
                    reply_markup=reply_markup
                )

                await callback_query.answer()

            except Exception as e:
                print(f"Error sending invoice: {e}")

                await callback_query.answer(
                    "🚫 Error Processing Your Payment. Try again.",
                    show_alert=True
                )

        else:
            await callback_query.answer(
                "⚠️ Invalid Premium Package.",
                show_alert=True
            )

    except Exception as e:
        print(f"Error In buy_ - {e}")


# Pre Checkout Handler
@Client.on_pre_checkout_query()
async def pre_checkout_handler(client, query: PreCheckoutQuery):
    try:
        if query.payload.startswith("dreamxpremium_"):
            await query.answer(success=True)

        else:
            await query.answer(
                success=False,
                error_message="⚠️ Invalid Purchase Type."
            )

    except Exception as e:
        print(f"Pre-checkout error: {e}")

        await query.answer(
            success=False,
            error_message="🚫 Unexpected Error Occurred."
        )


# Successful Star Payment
@Client.on_message(filters.successful_payment)
async def successful_premium_payment(client, message):
    try:
        amount = int(message.successful_payment.total_amount)
        user_id = message.from_user.id

        time_zone = datetime.datetime.now(
            pytz.timezone("Asia/Kolkata")
        )

        current_time = time_zone.strftime(
            "%d-%m-%Y | %I:%M:%S %p"
        )

        if amount in STAR_PREMIUM_PLANS:
            time = STAR_PREMIUM_PLANS[amount]
            seconds = await get_seconds(time)

            if seconds > 0:
                expiry_time = (
                    datetime.datetime.now()
                    + datetime.timedelta(seconds=seconds)
                )

                user_data = {
                    "id": user_id,
                    "expiry_time": expiry_time
                }

                await db.update_user(user_data)

                data = await db.get_user(user_id)
                expiry = data.get("expiry_time")

                expiry_str_in_ist = expiry.astimezone(
                    pytz.timezone("Asia/Kolkata")
                ).strftime(
                    "%d-%m-%Y | %I:%M:%S %p"
                )

                await message.reply_text(
                    f"Thankyou For Purchasing Premium Service "
                    f"Using Star ✅\n\n"
                    f"Subscribtion Time - {time}\n"
                    f"Expire In - {expiry_str_in_ist}",
                    disable_web_page_preview=True
                )

                await client.send_message(
                    PREMIUM_LOGS,
                    text=(
                        f"#Purchase_Premium_With_Star\n\n"
                        f"👤 ᴜꜱᴇʀ - {message.from_user.mention}\n\n"
                        f"⚡ ᴜꜱᴇʀ ɪᴅ - <code>{user_id}</code>\n\n"
                        f"🚫 ꜱᴛᴀʀ ᴘᴀʏ - {amount}⭐\n\n"
                        f"⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ - {time}\n\n"
                        f"⌛️ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ - {current_time}\n\n"
                        f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ - {expiry_str_in_ist}"
                    ),
                    disable_web_page_preview=True
                )

            else:
                await message.reply_text(
                    "⚠️ Invalid Premium Time."
                )

        else:
            await message.reply_text(
                "⚠️ Invalid Premium Package."
            )

    except Exception as e:
        print(f"Error Processing Premium Payment: {e}")

        await message.reply_text(
            "✅ Thank You For Your Payment! "
            "(Error Logging Details)"
        )


# Add Premium to ALL Registered Users
# Usage: /add_premium_all 1 day
@Client.on_message(
    filters.command("add_premium_all") & filters.user(ADMINS)
)
async def add_premium_all(client, message):

    if len(message.command) < 3:
        return await message.reply_text(
            "Usage: /add_premium_all 1 day"
        )

    time = " ".join(message.command[1:])
    seconds = await get_seconds(time)

    if seconds <= 0:
        return await message.reply_text(
            "Invalid time! Example: /add_premium_all 1 day"
        )

    now = datetime.datetime.now()
    users = await db.get_all_users()

    count = 0

    async for user_data in users:
        user_id = user_data.get("id")

        if not user_id:
            continue

        existing = await db.get_user(user_id)
        expiry = existing.get("expiry_time") if existing else None

        # Timezone-aware expiry ko safely handle karein
        if isinstance(expiry, datetime.datetime):
            if expiry.tzinfo is not None:
                expiry = expiry.replace(tzinfo=None)

            # Existing active Premium ko kam nahi karna
            if expiry > now:
                base_time = expiry
            else:
                base_time = now
        else:
            base_time = now

        expiry_time = base_time + datetime.timedelta(
            seconds=seconds
        )

        await db.update_user({
            "id": user_id,
            "expiry_time": expiry_time
        })

        count += 1

    await message.reply_text(
        f"🎉 Premium Gift Completed!\n\n"
        f"👥 Users: {count}\n"
        f"⏰ Duration: {time}"
    )
