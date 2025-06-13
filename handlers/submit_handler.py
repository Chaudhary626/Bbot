# handlers/submit_handler.py

def register(bot):
    from telebot import types
    from database import add_video, get_user_videos
    from config import MAX_VIDEO_LIMIT, MAX_DURATION_MINUTES

    user_states = {}

    @bot.message_handler(commands=['submit'])
    def handle_submit(message):
        user_id = message.from_user.id
        videos = get_user_videos(user_id)

        if len(videos) >= MAX_VIDEO_LIMIT:
            bot.send_message(user_id, f"🚫 You have reached the limit of {MAX_VIDEO_LIMIT} videos. Remove one to add new.")
            return

        user_states[user_id] = {'step': 'title'}
        bot.send_message(user_id, "📌 Please send your YouTube video *title*.", parse_mode='Markdown')

    @bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id, {}).get('step') == 'title')
    def get_title(message):
        user_states[message.from_user.id]['title'] = message.text
        user_states[message.from_user.id]['step'] = 'thumbnail'
        bot.send_message(message.chat.id, "🖼 Now send your *video thumbnail URL*.", parse_mode='Markdown')

    @bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id, {}).get('step') == 'thumbnail')
    def get_thumbnail(message):
        user_states[message.from_user.id]['thumbnail'] = message.text
        user_states[message.from_user.id]['step'] = 'duration'
        bot.send_message(message.chat.id, "⏱ Enter your video *duration in minutes* (e.g. 4.5).", parse_mode='Markdown')

    @bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id, {}).get('step') == 'duration')
    def get_duration(message):
        try:
            duration = float(message.text)
            if duration > MAX_DURATION_MINUTES:
                bot.send_message(message.chat.id, f"⚠️ Duration exceeds limit of {MAX_DURATION_MINUTES} minutes.")
                return
            user_states[message.from_user.id]['duration'] = duration
            user_states[message.from_user.id]['step'] = 'method'
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("link", "manual")
            bot.send_message(message.chat.id, "🔗 How should your video be accessed? (link/manual)", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, "❌ Invalid input. Please enter a valid number (e.g. 4.5).")

    @bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id, {}).get('step') == 'method')
    def get_method(message):
        method = message.text.strip().lower()
        if method not in ['link', 'manual']:
            bot.send_message(message.chat.id, "❌ Invalid option. Please choose 'link' or 'manual'.")
            return
        user_states[message.from_user.id]['method'] = method
        user_states[message.from_user.id]['step'] = 'link_or_instructions'

        if method == 'link':
            bot.send_message(message.chat.id, "🔗 Send your full YouTube *video link*.", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "📝 Describe how users can find your video manually.", parse_mode='Markdown')

    @bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id, {}).get('step') == 'link_or_instructions')
    def get_link_or_instructions(message):
        user_states[message.from_user.id]['link'] = message.text if user_states[message.from_user.id]['method'] == 'link' else ""
        user_states[message.from_user.id]['instructions'] = message.text if user_states[message.from_user.id]['method'] == 'manual' else ""
        user_states[message.from_user.id]['step'] = 'actions'

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("like", "subscribe", "comment", "share")
        bot.send_message(message.chat.id, "📋 Select *actions* you want from others (send comma-separated, e.g. like,comment).", reply_markup=markup, parse_mode='Markdown')

    @bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id, {}).get('step') == 'actions')
    def get_actions(message):
        actions = [a.strip().lower() for a in message.text.split(',') if a.strip()]
        if not actions:
            bot.send_message(message.chat.id, "❌ No actions selected. Please send again (e.g. like,comment).")
            return

        data = user_states.pop(message.from_user.id)
        add_video(
            user_id=message.from_user.id,
            title=data['title'],
            thumbnail=data['thumbnail'],
            duration=data['duration'],
            link=data.get('link', ''),
            actions=','.join(actions),
            method=data['method'],
            instructions=data.get('instructions', '')
        )

        bot.send_message(message.chat.id, "✅ Video submitted successfully! You can now help others using /match")
