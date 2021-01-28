import nltk

from pymystem3 import Mystem

from semantic_engine import SemanticEngine


try:
    nltk.corpus.stopwords.words('russian')
except LookupError:
    nltk.download('stopwords')


class Adviser:

    def __init__(
        self, base_url, prefix, channel_id, top_k, threshold, embeddings_path,
        corpus_path,
    ):
        self.prefix = prefix
        self.channel_id = channel_id
        self.top_k = top_k
        self.threshold = threshold
        self.base_url = base_url
        self.semantic_engine = SemanticEngine(embeddings_path, corpus_path)

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
        return '\n\n'.join([self.prefix, *threads])

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
        result = self.semantic_engine.get_top_k(query=text, top_k=self.top_k)
        thread_ids = [i['ts'] for i in result if i['score'] >= self.threshold]

        if not thread_ids:
            return

        return self.prepare_response_text(thread_ids)
