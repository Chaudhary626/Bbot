# handlers/admin_handler.py
from database import users_col, videos_col, reports_col, matches_col
from config import ADMIN_IDS

def register(bot):
    @bot.message_handler(commands=["admin"])
    def admin_panel(message):
        user_id = message.from_user.id
        if user_id not in ADMIN_IDS:
            bot.reply_to(message, "⛔ You are not authorized to access the admin panel.")
            return

        total_users = users_col.count_documents({})
        total_videos = videos_col.count_documents({})
        total_matches = matches_col.count_documents({"status": "pending"})
        total_reports = reports_col.count_documents({})

        msg = (
            f"👑 *Admin Panel*\n\n"
            f"👥 Total Users: `{total_users}`\n"
            f"🎥 Total Videos: `{total_videos}`\n"
            f"🔁 Active Matches: `{total_matches}`\n"
            f"🚨 Pending Reports: `{total_reports}`"
        )

        bot.send_message(user_id, msg, parse_mode='Markdown')
