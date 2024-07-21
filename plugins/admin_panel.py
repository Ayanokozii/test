from config import Config
from helper.database import db
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
import os
import sys
import time
import asyncio
import logging
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# User client for approving join requests (usable only by user, not bot)
user = Client(name="User", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.SESSION)


@Client.on_message(filters.command(["stats", "status"]) & filters.user(Config.ADMIN))
async def get_stats(bot, message):
    """Get bot statistics including uptime and total users."""
    total_users = await db.total_users_count()
    uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - Config.BOT_UPTIME))
    start_t = time.time()
    st = await message.reply('**Accessing the details...**')
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await st.edit(text=f"**--Bot Status--** \n\n**⌚️ Bot Uptime:** {uptime} \n**🐌 Current Ping:** `{time_taken_s:.3f} ms` \n**👭 Total Users:** `{total_users}`")


@Client.on_message(filters.private & filters.command("restart") & filters.user(Config.ADMIN))
async def restart_bot(b, m):
    """Restart the bot."""
    await m.reply_text("🔄__Restarting...__")
    os.execl(sys.executable, sys.executable, *sys.argv)


@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMIN) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    """Broadcast a message to all users."""
    await bot.send_message(Config.LOG_CHANNEL, f"{m.from_user.mention} or {m.from_user.id} has started the broadcast...")
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("Broadcast started...")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['id'], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            await db.delete_user(user['id'])
        done += 1
        if not done % 20:
            await sts_msg.edit(f"Broadcast in progress: \nTotal Users {total_users} \nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"Broadcast completed: \nCompleted in `{completed_in}`.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nFailed: {failed}")


async def send_msg(user_id, message):
    """Send a message to a user."""
    try:
        await message.forward(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Deactivated")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Blocked the bot")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : User ID invalid")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500


@Client.on_message(filters.private & filters.command('acceptall') & filters.user(Config.ADMIN))
async def handle_acceptall(bot: Client, message: Message):
    """Handle accepting all pending join requests."""
    ms = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
    chat_ids = await db.get_channel(Config.ADMIN)

    if not chat_ids:
        return await ms.edit("**I'm not admin in any Channel or Group yet!**")

    button = [
        [InlineKeyboardButton(f"{(await bot.get_chat(id)).title} {(str((await bot.get_chat(id)).type)).split('.')[1]}", callback_data=f'acceptallchat_{id}')]
        for id in chat_ids
    ]

    await ms.edit("Select Channel or Group below where you want to accept pending requests\n\nBelow Channels or Group I'm Admin there", reply_markup=InlineKeyboardMarkup(button))


@Client.on_message(filters.private & filters.command('declineall') & filters.user(Config.ADMIN))
async def handle_declineall(bot: Client, message: Message):
    """Handle declining all pending join requests."""
    ms = await message.reply_text("**Please Wait...**", reply_to_message_id=message.id)
    chat_ids = await db.get_channel(Config.ADMIN)

    if not chat_ids:
        return await ms.edit("**I'm not admin in any Channel or Group yet!**")

    button = [
        [InlineKeyboardButton(f"{(await bot.get_chat(id)).title} {(str((await bot.get_chat(id)).type)).split('.')[1]}", callback_data=f'declineallchat_{id}')]
        for id in chat_ids
    ]

    await ms.edit("Select Channel or Group below where you want to decline pending requests\n\nBelow Channels or Group I'm Admin there", reply_markup=InlineKeyboardMarkup(button))


@Client.on_callback_query(filters.regex('^acceptallchat_'))
async def handle_accept_pending_request(bot: Client, update: CallbackQuery):
    """Handle accepting all pending join requests for a specific chat."""
    chat_id = update.data.split('_')[1]
    ms = await update.message.edit("**Please Wait Accepting the pending requests. ♻️**")
    try:
        while True:
            try:
                await user.approve_all_chat_join_requests(chat_id=chat_id)
            except FloodWait as t:
                await asyncio.sleep(t.value)
                await user.approve_all_chat_join_requests(chat_id=chat_id)
            except Exception as e:
                logger.error(f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(e).__name__}, {e}")
                break
    finally:
        await ms.delete()
        await update.message.reply_text(f"**Task Completed** ✓ **Approved ✅ All Pending Join Requests**")


@Client.on_callback_query(filters.regex('^declineallchat_'))
async def handle_decline_pending_request(bot: Client, update: CallbackQuery):
    """Handle declining all pending join requests for a specific chat."""
    ms = await update.message.edit("**Please Wait Declining all the pending requests. ♻️**")
    chat_id = update.data.split('_')[1]

    try:
        while True:
            try:
                await user.decline_all_chat_join_requests(chat_id=chat_id)
            except FloodWait as t:
                await asyncio.sleep(t.value)
                await user.decline_all_chat_join_requests(chat_id=chat_id)
            except Exception as e:
                logger.error(f"Error on line {sys.exc_info()[-1].tb_lineno}: {type(e).__name__}, {e}")
                break
    finally:
        await ms.delete()
        await update.message.reply_text("**Task Completed** ✓ **Declined ❌ All The Pending Join Requests**")


# Run the bot
user.start()
print("User client started")
Client.run()
