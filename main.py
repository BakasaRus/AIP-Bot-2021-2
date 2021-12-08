import telebot
import twitch
import os

bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])
helix = twitch.Helix(os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Test')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(message)
    try:
        game_id = helix.game(name=message.text).id
        streams = helix.streams(game_id=game_id, first=5)
        for stream in streams:
            thumbnail = stream.thumbnail_url.format(width=640, height=480)
            caption = f'[{stream.title}](https://www.twitch.tv/{stream.user.display_name}/) ({stream.viewer_count} viewers)'
            bot.send_photo(message.chat.id, thumbnail, caption=caption, parse_mode='MARKDOWN')
    except twitch.helix.StreamNotFound:
        bot.reply_to(message, 'Streams are not found')
    except AttributeError:
        bot.reply_to(message, 'Not found')


bot.polling()
