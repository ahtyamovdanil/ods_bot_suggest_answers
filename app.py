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


@app.message(re.compile(r"\w*"))
def all_messages(client, message):
    logger.info(message)

    if message.get('thread_ts'):
        return

    client.chat_postMessage(
        text='<some response>',
        channel=message['channel'],
        thread_ts=message['ts'],
    )


if __name__ == "__main__":
    app.start(port=3000)
