# handlers/proof_handler.py

def register(bot):
    from database import submit_proof, has_active_task
    from telebot.types import Message

    @bot.message_handler(commands=['proof'])
    def handle_proof(message: Message):
        user_id = message.from_user.id

        if not has_active_task(user_id):
            bot.send_message(user_id, "🚫 You don't have any active task assigned.")
            return

        bot.send_message(user_id, "📤 Please upload your screen recording video file now.")

    @bot.message_handler(content_types=['video', 'document'])
    def receive_proof_file(message: Message):
        user_id = message.from_user.id

        if not has_active_task(user_id):
            bot.send_message(user_id, "❌ You have no active task. Use /match to get one.")
            return

        file_id = message.video.file_id if message.content_type == 'video' else message.document.file_id

        submit_proof(user_id, file_id)
        bot.send_message(user_id, "✅ Proof received. Waiting for the other user to verify it.")
