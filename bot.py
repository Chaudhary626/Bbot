### Step 1: Main Bot File (bot.py)

import telebot
from config import BOT_TOKEN
from handlers import start_handler, submit_handler, match_handler, proof_handler

bot = telebot.TeleBot(BOT_TOKEN)

# Register handlers
start_handler.register(bot)
submit_handler.register(bot)
match_handler.register(bot)
proof_handler.register(bot)

print("Bot is running...")
bot.infinity_polling()
