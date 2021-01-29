# import nltk
# from pymystem3 import Mystem
import requests
import os

ENGINE_IP = os.environ.get("ENGINE_IP")
ENGINE_PORT = os.environ.get("ENGINE_PORT")

# try:
#     nltk.corpus.stopwords.words("russian")
# except LookupError:
#     nltk.download("stopwords")


class Adviser:
    def __init__(
        self,
        base_url,
        prefix,
        channel_id,
        top_k,
        threshold
        # embeddings_path,
        # corpus_path,
    ):
        self.prefix = prefix
        self.channel_id = channel_id
        self.top_k = top_k
        self.threshold = threshold
        self.base_url = base_url
        # self.semantic_engine = SemanticEngine(embeddings_path, corpus_path)

        # TODO: попробовать лемматизировать и отбросить стоп-слова для корпуса
        # и текста запроса, см `common.preprocess_message`.
        # self.stem = Mystem()
        # self.stop_words = set(nltk.corpus.stopwords.words('russian'))

    def prepare_response_text(self, thread_ids):
        """
        Подготавливает текст ответа от имени бота.

        :param thread_ids:
            `list`, список идентификаторов на похожие треды.

        :return:
            `str`, текст ответа.
        """
        threads = [
            f'{self.base_url}/{self.channel_id}/p{ts.replace(".", "")}'
            for ts in thread_ids
        ]
        return "\n\n".join([self.prefix, *threads])

    def get_advice(self, text):
        """
        На основании переданного текста сообщения сформировать текст ответа с
        рекомендацией, который будет содержать ссылки на слак-треды канала
        `channel_id` с похожими обсуждениями.

        :param text:
            `str`, текст сообщения.

        :return:
            `str`, текст, который содержит ссылки на похожие треды канала или
            `None`, если не найдено рекомендации со скором выше установленного
            порога `threshold`.
        """
        result = requests.post(
            f"http://{ENGINE_IP}:{ENGINE_PORT}/api/get_messages",
            json={"text": text, "top_k": self.top_k},
        )
        thread_ids = [
            i["ts"] for i in result.json() if float(i["score"]) >= self.threshold
        ]
        thread_urls = [
            f'{self.base_url}/{self.channel_id}/p{ts.replace(".", "")}'
            for ts in thread_ids
        ]
        messages = [
            i["text"] for i in result.json() if float(i["score"]) >= self.threshold
        ]

        return thread_urls, messages


if __name__ == "__main__":
    # text = "Привет! Порекомендуйте, пожалуйста, бесплатные курсы для дата аналитиков? ML, Питон, SQL изучаю активно, хотела бы устроиться джуном в DS. Но последнее время все больше попадается вакансий на дата аналитика и кажется что здесь вход в профессию несколько легче. Во многих вакансиях помимо SQL и Python требуется продвинутый Excel, VBA, Tableau. Может есть какой-нибудь бесплатный курс, который быстро и понятно охватит эти темы?)"
    text = "Всем привет, посоветуйте курсы по python пожалуйста"
    adviser = Adviser(
        prefix="Посмотри похожие обсуждения:",
        channel_id="C04DP7BUY",
        base_url="https://opendatascience.slack.com/archives",
        top_k=3,
        threshold=0.8,
    )
    response = adviser.get_advice(text)
    print(response)

# C047H3DP4/p1611862151178100
# https://opendatascience.slack.com/archives/C04DP7BUY/p1611758847141500
