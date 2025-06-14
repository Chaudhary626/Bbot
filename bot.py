### Step 1: Main Bot File (bot.py)

import telebot
from config import BOT_TOKEN
from handlers import start_handler, submit_handler, match_handler, proof_handler
from handlers.video_handler import videos_handler, remove_video_callback
bot = telebot.TeleBot(BOT_TOKEN)

# Register handlers
start_handler.register(bot)
submit_handler.register(bot)
match_handler.register(bot)
proof_handler.register(bot)
dp.add_handler(CommandHandler("videos", videos_handler))
dp.add_handler(CallbackQueryHandler(remove_video_callback, pattern="^remove_video:"))

print("Bot is running...")
bot.infinity_polling()
