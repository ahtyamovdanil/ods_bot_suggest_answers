import os
import telebot
import telebot
import time
from adviser import Adviser
import os


token = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(token=token)

adviser = Adviser(
    prefix="Посмотри похожие обсуждения:",
    channel_id="C04DP7BUY",
    base_url="https://opendatascience.slack.com/archives",
    top_k=3,
    threshold=0.75,
)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    timestamps, messages = adviser.get_advice(message.text)
    if messages == []:
        bot.send_message(message.chat.id, "По вашему запросу ничего не найдено")
    else:
        for ts, m in zip(messages, timestamps):
            responce = "\n".join([ts, m])
            bot.send_message(message.chat.id, responce)


if __name__ == "__main__":
    bot.polling(none_stop=True)
