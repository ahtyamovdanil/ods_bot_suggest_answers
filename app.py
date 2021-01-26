import re
import os
import logging

import nltk

from pymystem3 import Mystem
from slack_bolt import App

from utils.common import prepare_response_text, preprocess_message


try:
    nltk.corpus.stopwords.words('russian')
except LookupError:
    nltk.download('stopwords')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')


STOP_WORDS = set(nltk.corpus.stopwords.words('russian'))
STEM = Mystem()


app = App(
    name='ODS bot suggest answers',
    logger=logger,
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.message(re.compile(r"\w*"))
def non_thread_message(client, message):
    logger.info(message)

    # пропускаем сообщения, которые отправлены в треды
    if message.get('thread_ts'):
        return

    text = message.get('text')
    if not text:
        return

    msg = preprocess_message(text, STEM, STOP_WORDS)
    logger.info(msg)

    prefix = 'Посмотри похожие обсуждения:'
    suggestion = [
        'https://opendatascience.slack.com/archives/'
        'C04DP7BUY/p1611478116040000'
    ] * 5

    client.chat_postMessage(
        text=prepare_response_text(prefix, suggestion),
        channel=message['channel'],
        thread_ts=message['ts'],
    )


# заглушка для всех остальных event по сообщениям
@app.event({'type': 'message'})
def just_ack():
    return


if __name__ == "__main__":
    app.start(port=3000)
