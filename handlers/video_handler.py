# handlers/video_handler.py
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_user_videos, delete_video_by_id

def register(bot):
    @bot.message_handler(commands=["videos"])
    def videos_handler(message):
        user_id = message.from_user.id
        videos = get_user_videos(user_id)

        if not videos:
            bot.send_message(user_id, "❌ You haven't submitted any videos yet.")
            return

        for video in videos:
            title = video.get("title")
            thumb_url = video.get("thumbnail")
            video_id = str(video.get("_id"))

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("🗑️ Remove", callback_data=f"remove_video:{video_id}"))

            bot.send_photo(chat_id=user_id, photo=thumb_url, caption=f"🎥 *{title}*", reply_markup=markup, parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("remove_video:"))
    def remove_video_callback(call):
        video_id = call.data.split(":")[1]
        success = delete_video_by_id(video_id)

        if success:
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     caption="✅ Video removed successfully.")
        else:
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     caption="❌ Failed to remove video.")
