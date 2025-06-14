import telebot
from config import BOT_TOKEN
from handlers import start_handler, submit_handler, match_handler, proof_handler
from handlers import video_handler  # <- this line

bot = telebot.TeleBot(BOT_TOKEN)

# Register handlers
start_handler.register(bot)
submit_handler.register(bot)
match_handler.register(bot)
proof_handler.register(bot)
video_handler.register(bot)  # <-- 👈 important fix

print("Bot is running...")
bot.infinity_polling()
