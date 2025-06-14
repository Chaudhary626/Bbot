# handlers/video_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from database import get_user_videos, delete_video_by_id

def videos_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    videos = get_user_videos(user_id)

    if not videos:
        update.message.reply_text("\u274C You haven't submitted any videos yet.")
        return

    for video in videos:
        title = video.get("title")
        thumb_url = video.get("thumbnail")
        video_id = str(video.get("_id"))

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("\ud83d\uddd1\ufe0f Remove", callback_data=f"remove_video:{video_id}")]
        ])

        context.bot.send_photo(
            chat_id=user_id,
            photo=thumb_url,
            caption=f"\ud83c\udfa5 *{title}*",
            parse_mode="Markdown",
            reply_markup=keyboard
        )

def remove_video_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    data = query.data
    if not data.startswith("remove_video:"):
        return

    video_id = data.split(":")[1]
    success = delete_video_by_id(video_id)

    if success:
        query.edit_message_caption("\u2705 Video removed successfully.")
    else:
        query.edit_message_caption("\u274C Failed to remove video. Try again later.")

# Register these handlers in bot.py like this:
# from handlers.video_handler import videos_handler, remove_video_callback
# dp.add_handler(CommandHandler("videos", videos_handler))
# dp.add_handler(CallbackQueryHandler(remove_video_callback, pattern="^remove_video:"))
