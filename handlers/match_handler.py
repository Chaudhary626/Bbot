# handlers/match_handler.py

def register(bot):
    from database import assign_video_to_user, get_pending_tasks, update_last_active

    @bot.message_handler(commands=['match'])
    def handle_match(message):
        user_id = message.from_user.id
        update_last_active(user_id)

        video = assign_video_to_user(user_id)
        if not video:
            bot.send_message(user_id, "🕒 No videos available right now. Please try again later.")
            return

        if video['method'] == 'manual':
            access_instructions = f"🔍 *Search Instructions:*\n{video['instructions']}"
        else:
            access_instructions = f"🔗 *Link (don't click, open YouTube manually):*\n{video['link']}"

        actions_text = ', '.join(video['actions'].split(','))

        task_msg = f"""
🎯 *New Task Assigned!*

📺 *Title:* {video['title']}
🖼 *Thumbnail:* [Thumbnail]({video['thumbnail']})
⏱ *Duration:* {video['duration']} min
{access_instructions}

✅ *Actions Required:* {actions_text}

🎥 *Please record your screen while watching this video.*
Once done, upload your recording using /proof
        """
        bot.send_message(user_id, task_msg, parse_mode='Markdown', disable_web_page_preview=False)
