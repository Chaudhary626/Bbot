# handlers/start_handler.py

def register(bot):
    from database import add_user, update_last_active

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        user_id = message.from_user.id
        username = message.from_user.username or "no_username"

        # Register or update user
        add_user(user_id, username)
        update_last_active(user_id)

        # Welcome message with rules
        welcome_msg = f"""
👋 Welcome {username}!

📌 *Rules & Warnings:*
- Video must be under 5 minutes.
- You must help others to get help.
- Proof (screen recording) is mandatory.

✅ *How it works:*
1. Submit your video details.
2. Accept to help a random user.
3. Watch their video with screen recording.
4. Submit proof.
5. When they verify, your task is unlocked.

Type /submit to begin!
        """
        bot.send_message(user_id, welcome_msg, parse_mode='Markdown')
