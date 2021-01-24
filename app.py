import re
import os
import logging

from slack_bolt import App


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')


app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


def prepare_text(suggestion):
    text = ['Посмотри похожие обсуждения:']
    text.extend(suggestion)
    return '\n\n'.join(text)


@app.message(re.compile(r"\w*"))
def non_thread_message(client, message):
    logger.info(message)

    # пропускаем сообщения, которые отправлены в треды
    if message.get('thread_ts'):
        return

    suggestion = [
        'https://opendatascience.slack.com/archives/'
        'C04DP7BUY/p1611478116040000'
    ] * 5

    client.chat_postMessage(
        text=prepare_text(suggestion),
        channel=message['channel'],
        thread_ts=message['ts'],
    )


# заглушка для всех остальных event по сообщениям
@app.event({'type': 'message'})
def just_ack():
    return


if __name__ == "__main__":
    app.start(port=3000)
