import re
import os
import logging

from slack_bolt import App

from adviser import Adviser


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')


app = App(
    name='ODS bot suggest answers',
    logger=logger,
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)

# FIXME: вынести параметры в конфиг файл
adviser = Adviser(
    prefix='Посмотри похожие обсуждения:',
    channel_id='C04DP7BUY',
    base_url='https://opendatascience.slack.com/archives',
    top_k=3,
    threshold=0.8,
    corpus_path='./data/prepared/corpus_df.pickle',
    embeddings_path='./data/prepared/embeddings.pt',
)


@app.message(re.compile(r"\w*"))
def non_thread_message(client, message):
    logger.info(message)

    # пропускаем сообщения, которые отправлены в треды
    if message.get('thread_ts'):
        return

    text = message.get('text')
    # в норме такого быть не должно
    if not text:
        return

    test_response = adviser.get_advice(text)
    # не найдены похожие треды, который бы удовлетворяли threshold
    if not test_response:
        return

    client.chat_postMessage(
        text=test_response,
        channel=message['channel'],
        thread_ts=message['ts'],
    )


# заглушка для всех остальных event по сообщениям
@app.event({'type': 'message'})
def just_ack():
    return


if __name__ == "__main__":
    app.start(port=3000)
