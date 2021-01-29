import os
import telebot
import telebot
from adviser import Adviser
import os


token = os.environ.get("BOT_TOKEN")
port = os.environ.get("ENGINE_PORT")

bot = telebot.TeleBot(token=token)

# ENGINE_IP = "0.0.0.0"
# ENGINE_PORT = "8989"

adviser = Adviser(
    prefix="Посмотри похожие обсуждения:",
    channel_id="C04DP7BUY",
    base_url="https://opendatascience.slack.com/archives",
    top_k=3,
    threshold=0.75,
)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    response = adviser.get_advice(message.text)
    bot.send_message(message.chat.id, response)


if __name__ == "__main__":
    bot.polling(none_stop=True)
